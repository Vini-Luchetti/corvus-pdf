#!/usr/bin/env python3
"""
CORVUS PDF v1.0
Corvus Labs — geralzona.com

MESCLAR:  N PDFs + seleção de páginas por arquivo → 1 PDF
SEPARAR:  1+ PDFs → N PDFs (todas as páginas ou ranges específicos)

Sintaxe de páginas: "1-3, 5, 7-9" — mesma do Windows ao imprimir.
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader, PdfWriter

# ── DPI awareness (Windows) ────────────────────────────────────────
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ── Paleta âmbar CRT ──────────────────────────────────────────────
BG    = '#0a0602'   # fundo principal
BGD   = '#080602'   # fundo escuro (header, inputs)
BGROW = '#100806'   # linhas alternadas
BOR   = '#3a1e08'   # borda padrão
BORA  = '#994400'   # borda/label ativo
DIM   = '#bb7722'   # texto secundário (legível, mas recuado)
MID   = '#dd9933'   # texto médio
TXT   = '#ffaa33'   # texto principal (âmbar)
BRT   = '#ffd080'   # texto claro (filenames)
RED   = '#ff6644'   # botão remover
BBG   = '#ffaa33'   # bg do botão PROCESSAR
BFG   = '#080602'   # fg do botão PROCESSAR

MONO  = ('Courier New', 10)
MONOS = ('Courier New', 9)
MONOB = ('Courier New', 12, 'bold')


# ── Utilitário de páginas ──────────────────────────────────────────

def parse_pages(s: str, total: int) -> list:
    """
    Converte string de seleção de páginas em lista 0-indexada.
    Suporta: '1-3, 5, 7-9'  /  '1;3;5-8'  /  vazio = todas
    """
    if not s.strip():
        return list(range(total))
    pages: set = set()
    for part in s.replace(';', ',').split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                a, b = int(a.strip()), int(b.strip())
                pages.update(range(max(1, a) - 1, min(total, b)))
            except ValueError:
                pass
        else:
            try:
                n = int(part)
                if 1 <= n <= total:
                    pages.add(n - 1)
            except ValueError:
                pass
    return sorted(pages)


# ── Aplicação ─────────────────────────────────────────────────────

class CorvusPDF(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('CORVUS PDF')
        self.configure(bg=BGD)
        self.minsize(720, 580)

        # State vars
        self.out_folder_b  = tk.StringVar()
        self.out_folder_s  = tk.StringVar()
        self.out_name_b    = tk.StringVar(value='resultado.pdf')
        self.split_mode    = tk.StringVar(value='all')
        self.build_files   = []   # [{'path','total','pages_var','frame'}]
        self.split_files   = []   # [{'path','total','frame'}]
        self.split_ranges  = []   # [{'var','frame'}]

        self._build_header()
        self._build_tabbar()

        self.pane_b = tk.Frame(self, bg=BG, padx=14, pady=10)
        self.pane_s = tk.Frame(self, bg=BG, padx=14, pady=10)
        self._build_construir()
        self._build_explodir()
        self._switch('build')

    # ── Helpers compartilhados ────────────────────────────────────

    def _section(self, parent, text):
        """Label de seção com linha separadora."""
        row = tk.Frame(parent, bg=BG)
        row.pack(fill='x', pady=(8, 4))
        tk.Label(row, text=f'// {text}', font=MONOS,
                 bg=BG, fg=BORA).pack(side='left')
        tk.Frame(row, bg=BOR, height=1).pack(
            side='left', fill='x', expand=True, padx=(8, 0))

    def _make_btn(self, parent, text, cmd, **kw):
        return tk.Button(
            parent, text=text, command=cmd, font=MONOS,
            bg=BG, fg=TXT, activebackground=BORA, activeforeground=BFG,
            relief='flat', cursor='hand2',
            highlightbackground=BOR, highlightthickness=1,
            padx=8, pady=3, **kw)

    def _make_log(self, parent) -> tk.Text:
        outer = tk.Frame(parent, bg=BOR, padx=1, pady=1)
        outer.pack(fill='x', pady=(6, 0))
        t = tk.Text(outer, height=4, font=MONOS, bg='#060402', fg=DIM,
                    relief='flat', state='disabled', wrap='word')
        t.pack(fill='both')
        return t

    def _log(self, widget, msg: str):
        """Thread-safe: escreve no log."""
        def _upd():
            widget.config(state='normal')
            widget.insert('end', msg + '\n')
            widget.see('end')
            widget.config(state='disabled')
        self.after(0, _upd)

    def _clear_log(self, widget):
        widget.config(state='normal')
        widget.delete('1.0', 'end')
        widget.config(state='disabled')

    def _process_btn(self, parent, cmd):
        tk.Button(
            parent, text='▶  PROCESSAR', command=cmd,
            font=MONOB, bg=BBG, fg=BFG,
            activebackground='#dd8800', activeforeground=BFG,
            relief='flat', cursor='hand2', pady=9
        ).pack(fill='x', pady=(8, 0))

    # ── Header & Tabs ─────────────────────────────────────────────

    def _build_header(self):
        f = tk.Frame(self, bg=BGD, height=34)
        f.pack(fill='x')
        f.pack_propagate(False)

        c = tk.Canvas(f, bg=BGD, width=64, height=34, highlightthickness=0)
        c.pack(side='left', padx=10)
        for i, col in enumerate(('#ff5f57', '#febc2e', '#28c840')):
            x = 6 + i * 18
            c.create_oval(x, 11, x + 12, 23, fill=col, outline='')

        tk.Label(f, text='CORVUS PDF // v1.0', font=MONO,
                 bg=BGD, fg=TXT).pack(side='left')
        tk.Label(f, text='CORVUS LABS — geralzona.com', font=MONOS,
                 bg=BGD, fg=DIM).pack(side='right', padx=14)

    def _build_tabbar(self):
        bar = tk.Frame(self, bg=BGD)
        bar.pack(fill='x')
        inner = tk.Frame(bar, bg=BGD)
        inner.pack(side='left', padx=14, pady=(4, 0))

        self._tb = tk.Label(inner, text='▶ MESCLAR', font=MONOS,
                            cursor='hand2', padx=14, pady=5)
        self._tb.pack(side='left')
        self._tb.bind('<Button-1>', lambda _: self._switch('build'))

        self._ts = tk.Label(inner, text='SEPARAR', font=MONOS,
                            cursor='hand2', padx=14, pady=5)
        self._ts.pack(side='left', padx=(2, 0))
        self._ts.bind('<Button-1>', lambda _: self._switch('split'))

        tk.Frame(self, bg=BOR, height=1).pack(fill='x')

    def _switch(self, tab: str):
        if tab == 'build':
            self._tb.config(bg=BBG, fg=BFG)
            self._ts.config(bg=BGD, fg=MID)
            self.pane_s.pack_forget()
            self.pane_b.pack(fill='both', expand=True)
        else:
            self._ts.config(bg=BBG, fg=BFG)
            self._tb.config(bg=BGD, fg=MID)
            self.pane_b.pack_forget()
            self.pane_s.pack(fill='both', expand=True)

    # ── CONSTRUIR ─────────────────────────────────────────────────

    def _build_construir(self):
        p = self.pane_b
        self._section(p, 'ARQUIVOS  ·  PÁGINAS (vazio = todas)')

        # Lista com borda e scroll
        outer = tk.Frame(p, bg=BOR, padx=1, pady=1)
        outer.pack(fill='both', expand=True)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill='both', expand=True)

        self._bc = tk.Canvas(inner, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(inner, orient='vertical', command=self._bc.yview,
                           bg=BGD, troughcolor=BGD, activebackground=MID)
        vsb.pack(side='right', fill='y')
        self._bc.pack(fill='both', expand=True)
        self._bc.configure(yscrollcommand=vsb.set)

        self._brf = tk.Frame(self._bc, bg=BG)
        self._bcw = self._bc.create_window((0, 0), window=self._brf, anchor='nw')
        self._brf.bind('<Configure>', lambda e: self._bc.configure(
            scrollregion=self._bc.bbox('all')))
        self._bc.bind('<Configure>', lambda e: self._bc.itemconfig(
            self._bcw, width=e.width))
        self._bc.bind('<MouseWheel>', lambda e: self._bc.yview_scroll(
            -1 * (e.delta // 120), 'units'))

        # Botão adicionar
        add_f = tk.Frame(inner, bg=BGD)
        add_f.pack(fill='x')
        tk.Frame(add_f, bg=BOR, height=1).pack(fill='x')
        lbl = tk.Label(add_f, text='  + ADICIONAR PDF', font=MONOS,
                       bg=BGD, fg=BORA, cursor='hand2', pady=6, anchor='w')
        lbl.pack(fill='x')
        lbl.bind('<Button-1>', lambda _: self._add_build_file())

        # Saída
        self._section(p, 'SAÍDA')

        r1 = tk.Frame(p, bg=BG)
        r1.pack(fill='x', pady=(0, 4))
        ef = tk.Frame(r1, bg=BOR, padx=1, pady=1)
        ef.pack(side='left', fill='x', expand=True, padx=(0, 6))
        tk.Entry(ef, textvariable=self.out_folder_b, font=MONOS,
                 bg=BGD, fg=DIM, insertbackground=TXT,
                 relief='flat').pack(fill='x', ipady=4, padx=4)
        self._make_btn(r1, 'PASTA', self._pick_folder_b).pack(side='left')

        r2 = tk.Frame(p, bg=BG)
        r2.pack(fill='x')
        tk.Label(r2, text='NOME:', font=MONOS, bg=BG, fg=DIM,
                 width=7).pack(side='left')
        nf = tk.Frame(r2, bg=BOR, padx=1, pady=1)
        nf.pack(side='left', fill='x', expand=True)
        tk.Entry(nf, textvariable=self.out_name_b, font=MONOS,
                 bg=BGD, fg=BRT, insertbackground=TXT,
                 relief='flat').pack(fill='x', ipady=4, padx=4)

        self._blog = self._make_log(p)
        self._process_btn(p, self._run_construir)

    def _add_build_file(self):
        paths = filedialog.askopenfilenames(
            title='Selecionar PDFs', filetypes=[('PDF', '*.pdf')])
        for path in paths:
            try:
                total = len(PdfReader(path).pages)
            except Exception as e:
                self._log(self._blog, f'✕  Erro ao ler {os.path.basename(path)}: {e}')
                continue
            pages_var = tk.StringVar()
            idx = len(self.build_files)
            frame = self._make_build_row(path, total, pages_var, idx)
            self.build_files.append({'path': path, 'total': total,
                                     'pages_var': pages_var, 'frame': frame})
            if not self.out_folder_b.get():
                self.out_folder_b.set(os.path.dirname(os.path.abspath(path)))

    def _make_build_row(self, path, total, pages_var, idx):
        bg = BGROW if idx % 2 == 0 else BG
        row = tk.Frame(self._brf, bg=bg)
        row.pack(fill='x')
        tk.Frame(row, bg=BOR, height=1).pack(fill='x')

        inner = tk.Frame(row, bg=bg)
        inner.pack(fill='x', padx=8, pady=5)

        tk.Label(inner, text=f'{idx+1:02d}', font=MONOS,
                 bg=bg, fg=MID, width=3).pack(side='left')

        name = os.path.basename(path)
        if len(name) > 33:
            name = name[:30] + '...'
        tk.Label(inner, text=name, font=MONOS, bg=bg, fg=BRT,
                 anchor='w', width=33).pack(side='left')

        tk.Label(inner, text=f'{total}p', font=MONOS,
                 bg=bg, fg=DIM, width=5).pack(side='left')

        pf = tk.Frame(inner, bg=BOR, padx=1, pady=1)
        pf.pack(side='left', padx=(0, 6))
        tk.Entry(pf, textvariable=pages_var, font=MONOS,
                 bg=BGD, fg=TXT, insertbackground=TXT,
                 relief='flat', width=12).pack(ipady=3, padx=2)

        # Captura idx por default arg para evitar closure errada
        tk.Button(inner, text='↑', font=MONOS, bg=bg, fg=TXT,
                  relief='flat', cursor='hand2', padx=4, pady=1,
                  command=lambda i=idx: self._build_move(i, -1)
                  ).pack(side='left', padx=1)
        tk.Button(inner, text='↓', font=MONOS, bg=bg, fg=TXT,
                  relief='flat', cursor='hand2', padx=4, pady=1,
                  command=lambda i=idx: self._build_move(i, 1)
                  ).pack(side='left', padx=1)
        tk.Button(inner, text='✕', font=MONOS, bg=bg, fg=RED,
                  relief='flat', cursor='hand2', padx=4, pady=1,
                  command=lambda i=idx: self._build_remove(i)
                  ).pack(side='left', padx=1)
        return row

    def _rebuild_build_rows(self):
        for w in self._brf.winfo_children():
            w.destroy()
        snapshot = [(f['path'], f['total'], f['pages_var'].get())
                    for f in self.build_files]
        self.build_files = []
        for i, (path, total, pg) in enumerate(snapshot):
            pv = tk.StringVar(value=pg)
            frame = self._make_build_row(path, total, pv, i)
            self.build_files.append({'path': path, 'total': total,
                                     'pages_var': pv, 'frame': frame})

    def _build_move(self, idx, direction):
        new_i = idx + direction
        if 0 <= new_i < len(self.build_files):
            lst = self.build_files
            lst[idx], lst[new_i] = lst[new_i], lst[idx]
            self._rebuild_build_rows()

    def _build_remove(self, idx):
        self.build_files.pop(idx)
        self._rebuild_build_rows()

    def _pick_folder_b(self):
        d = filedialog.askdirectory(title='Pasta de saída')
        if d:
            self.out_folder_b.set(d)

    def _run_construir(self):
        if not self.build_files:
            self._log(self._blog, '✕  Nenhum arquivo na lista.')
            return
        folder = self.out_folder_b.get() or os.getcwd()
        name   = self.out_name_b.get().strip() or 'resultado.pdf'
        if not name.lower().endswith('.pdf'):
            name += '.pdf'
        # Snapshot thread-safe antes de processar
        snapshot = [{'path': f['path'], 'total': f['total'],
                     'pages': f['pages_var'].get()}
                    for f in self.build_files]
        self._clear_log(self._blog)
        self._log(self._blog, f'Montando {len(snapshot)} arquivo(s)...')
        threading.Thread(target=self._do_construir,
                         args=(folder, name, snapshot), daemon=True).start()

    def _do_construir(self, folder, name, snapshot):
        try:
            writer = PdfWriter()
            total_pg = 0
            for f in snapshot:
                reader = PdfReader(f['path'])
                pages  = parse_pages(f['pages'], f['total'])
                base   = os.path.basename(f['path'])
                self._log(self._blog, f'→ {base}  [{len(pages)} pág.]')
                for p in pages:
                    writer.add_page(reader.pages[p])
                total_pg += len(pages)
            out_path = os.path.join(folder, name)
            with open(out_path, 'wb') as fout:
                writer.write(fout)
            writer.close()
            self._log(self._blog, f'\n✓  {total_pg} páginas → {out_path}')
        except Exception as e:
            self._log(self._blog, f'\n✕  Erro: {e}')

    # ── EXPLODIR ──────────────────────────────────────────────────

    def _build_explodir(self):
        p = self.pane_s
        self._section(p, 'ARQUIVO')

        outer = tk.Frame(p, bg=BOR, padx=1, pady=1)
        outer.pack(fill='x')
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill='both')

        self._srf = tk.Frame(inner, bg=BG)
        self._srf.pack(fill='x')

        add_f = tk.Frame(inner, bg=BGD)
        add_f.pack(fill='x')
        tk.Frame(add_f, bg=BOR, height=1).pack(fill='x')
        lbl = tk.Label(add_f, text='  + ADICIONAR PDF', font=MONOS,
                       bg=BGD, fg=BORA, cursor='hand2', pady=6, anchor='w')
        lbl.pack(fill='x')
        lbl.bind('<Button-1>', lambda _: self._add_split_file())

        # Modo
        self._section(p, 'MODO')
        mf = tk.Frame(p, bg=BG)
        mf.pack(fill='x')
        rb_kw = dict(font=MONO, bg=BG, fg=BRT, selectcolor=BGD,
                     activebackground=BG, variable=self.split_mode)
        tk.Radiobutton(mf, text='Todas as páginas  (uma por arquivo)',
                       value='all', command=self._toggle_ranges,
                       **rb_kw).pack(anchor='w')
        tk.Radiobutton(mf, text='Ranges específicos  (um arquivo por range)',
                       value='ranges', command=self._toggle_ranges,
                       **rb_kw).pack(anchor='w', pady=(4, 0))

        # Container de ranges (oculto por padrão)
        self._ranges_outer = tk.Frame(p, bg=BG, padx=24)
        self._ranges_frame = tk.Frame(self._ranges_outer, bg=BG)
        self._ranges_frame.pack(fill='x')
        add_r = tk.Label(self._ranges_outer, text='+ RANGE', font=MONOS,
                         bg=BG, fg=BORA, cursor='hand2', anchor='w')
        add_r.pack(anchor='w', pady=(4, 0))
        add_r.bind('<Button-1>', lambda _: self._add_range())

        # Saída
        self._section(p, 'SAÍDA')
        row = tk.Frame(p, bg=BG)
        row.pack(fill='x', pady=(0, 4))
        ef = tk.Frame(row, bg=BOR, padx=1, pady=1)
        ef.pack(side='left', fill='x', expand=True, padx=(0, 6))
        tk.Entry(ef, textvariable=self.out_folder_s, font=MONOS,
                 bg=BGD, fg=DIM, insertbackground=TXT,
                 relief='flat').pack(fill='x', ipady=4, padx=4)
        self._make_btn(row, 'PASTA', self._pick_folder_s).pack(side='left')

        self._slog = self._make_log(p)
        self._process_btn(p, self._run_explodir)

    def _add_split_file(self):
        paths = filedialog.askopenfilenames(
            title='Selecionar PDFs', filetypes=[('PDF', '*.pdf')])
        for path in paths:
            try:
                total = len(PdfReader(path).pages)
            except Exception as e:
                self._log(self._slog, f'✕  Erro ao ler {os.path.basename(path)}: {e}')
                continue
            idx = len(self.split_files)
            frame = self._make_split_row(path, total, idx)
            self.split_files.append({'path': path, 'total': total, 'frame': frame})
            if not self.out_folder_s.get():
                self.out_folder_s.set(os.path.dirname(os.path.abspath(path)))

    def _make_split_row(self, path, total, idx):
        bg = BGROW if idx % 2 == 0 else BG
        row = tk.Frame(self._srf, bg=bg)
        row.pack(fill='x')
        tk.Frame(row, bg=BOR, height=1).pack(fill='x')
        inner = tk.Frame(row, bg=bg)
        inner.pack(fill='x', padx=8, pady=5)

        name = os.path.basename(path)
        if len(name) > 44:
            name = name[:41] + '...'
        tk.Label(inner, text=name, font=MONOS, bg=bg, fg=BRT,
                 anchor='w', width=44).pack(side='left')
        tk.Label(inner, text=f'{total} pág.', font=MONOS,
                 bg=bg, fg=DIM, width=8).pack(side='left')

        def rm(i=idx):
            self.split_files.pop(i)
            self._rebuild_split_rows()

        tk.Button(inner, text='✕', font=MONOS, bg=bg, fg=RED,
                  relief='flat', cursor='hand2', padx=4,
                  command=rm).pack(side='right')
        return row

    def _rebuild_split_rows(self):
        for w in self._srf.winfo_children():
            w.destroy()
        snapshot = [(f['path'], f['total']) for f in self.split_files]
        self.split_files = []
        for i, (path, total) in enumerate(snapshot):
            frame = self._make_split_row(path, total, i)
            self.split_files.append({'path': path, 'total': total, 'frame': frame})

    def _toggle_ranges(self):
        if self.split_mode.get() == 'ranges':
            self._ranges_outer.pack(fill='x', pady=(4, 0))
            if not self.split_ranges:
                self._add_range()
        else:
            self._ranges_outer.pack_forget()

    def _add_range(self):
        i = len(self.split_ranges)
        var = tk.StringVar()
        row = tk.Frame(self._ranges_frame, bg=BG)
        row.pack(fill='x', pady=2)

        tk.Label(row, text=f'RANGE {i+1:02d}:', font=MONOS,
                 bg=BG, fg=DIM, width=10).pack(side='left')
        rf = tk.Frame(row, bg=BOR, padx=1, pady=1)
        rf.pack(side='left')
        tk.Entry(rf, textvariable=var, font=MONOS,
                 bg=BGD, fg=TXT, insertbackground=TXT,
                 relief='flat', width=14).pack(ipady=3, padx=2)

        suffix_lbl = tk.Label(row, text=f'→ arquivo_{i+1:02d}.pdf',
                              font=MONOS, bg=BG, fg=DIM)
        suffix_lbl.pack(side='left', padx=(8, 0))

        def rm(i=i):
            self.split_ranges.pop(i)
            self._rebuild_ranges()

        tk.Button(row, text='✕', font=MONOS, bg=BG, fg=RED,
                  relief='flat', cursor='hand2', padx=4,
                  command=rm).pack(side='left', padx=4)

        self.split_ranges.append({'var': var, 'frame': row})

    def _rebuild_ranges(self):
        for w in self._ranges_frame.winfo_children():
            w.destroy()
        vals = [r['var'].get() for r in self.split_ranges]
        self.split_ranges = []
        for v in vals:
            self._add_range()
            self.split_ranges[-1]['var'].set(v)

    def _pick_folder_s(self):
        d = filedialog.askdirectory(title='Pasta de saída')
        if d:
            self.out_folder_s.set(d)

    def _run_explodir(self):
        if not self.split_files:
            self._log(self._slog, '✕  Nenhum arquivo na lista.')
            return
        folder       = self.out_folder_s.get() or os.getcwd()
        mode         = self.split_mode.get()
        files_snap   = list(self.split_files)
        ranges_snap  = [r['var'].get() for r in self.split_ranges]
        self._clear_log(self._slog)
        threading.Thread(target=self._do_explodir,
                         args=(folder, mode, files_snap, ranges_snap),
                         daemon=True).start()

    def _do_explodir(self, folder, mode, files, ranges_vals):
        try:
            total_out = 0
            for f in files:
                reader = PdfReader(f['path'])
                base   = os.path.splitext(os.path.basename(f['path']))[0]
                total  = f['total']
                self._log(self._slog, f'→ {base}.pdf  ({total} pág.)')

                if mode == 'all':
                    for i, page in enumerate(reader.pages):
                        writer = PdfWriter()
                        writer.add_page(page)
                        out = os.path.join(folder, f'{base}_p{i+1:03d}.pdf')
                        with open(out, 'wb') as fout:
                            writer.write(fout)
                        writer.close()
                        total_out += 1
                    self._log(self._slog, f'  ✓ {total} arquivo(s) gerado(s)')
                else:
                    for i, rng in enumerate(ranges_vals):
                        pages = parse_pages(rng, total)
                        if not pages:
                            self._log(self._slog,
                                      f'  ⚠  Range {i+1} vazio ou inválido, ignorado.')
                            continue
                        writer = PdfWriter()
                        for p in pages:
                            writer.add_page(reader.pages[p])
                        out = os.path.join(folder, f'{base}_{i+1:02d}.pdf')
                        with open(out, 'wb') as fout:
                            writer.write(fout)
                        writer.close()
                        self._log(self._slog,
                                  f'  ✓ Range {i+1} ({len(pages)} pág.) '
                                  f'→ {os.path.basename(out)}')
                        total_out += 1

            self._log(self._slog,
                      f'\n✓  {total_out} arquivo(s) gerado(s) em:\n   {folder}')
        except Exception as e:
            self._log(self._slog, f'\n✕  Erro: {e}')


if __name__ == '__main__':
    app = CorvusPDF()
    app.mainloop()
