from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

pdf = MarkdownPdf(toc_level=2)
pdf.add_section(Section("# Title\n", toc=False))
pdf.add_section(Section("# Head1\n\nbody\n"))
pdf.add_section(Section("## Head2\n\n### Head3\n\n"))

pdf.meta["title"] = "User Guide"

pdf.save("guide.pdf")
