"""PDF 2 Pocketmod - A command-line tool for converting a pdf file to a pocketmod arrangement."""

import click
import fitz


@click.group()
def cli():
    """PDF 2 Pocketmod"""
    pass

@cli.command()
@click.argument('input_pdf', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default='output.pdf')
@click.option('--start-page', '-s', type=int, default=0, help='The page to start from.')
def create(input_pdf, output, start_page):
    """Create a pocketmod file."""
    # Open the input PDF
    try:
        doc = fitz.open(input_pdf)
    except Exception as e:
        click.echo(f"Error opening input PDF: {e}", err=True)
        return False

    # Check if we have enough pages
    page_count = len(doc)
    if page_count < 8:
        click.echo(
            f"Warning: Input PDF has only {page_count} pages, but 8 pages are needed.", err=True)
        click.echo("Missing pages will be blank.", err=True)

    # Create a new PDF with a single page in landscape orientation
    out_doc = fitz.open()
    page_size = fitz.paper_rect("a4-l")  # A4 in landscape orientation
    out_page = out_doc.new_page(width=page_size.width, height=page_size.height)

    # Define the positions and rotations for the 8 pages in pocketmod layout
    # The order matters for proper folding
    # Each tuple contains: (page_number, rotation, position_x, position_y, scale)
    page_layout = [
        (6, 180, 0.00, 0.00, 0.5),  # Page 7
        (5, 180, 0.25, 0.00, 0.5),  # Page 6
        (4, 180, 0.50, 0.00, 0.5),  # Page 5
        (3, 180, 0.75, 0.00, 0.5),  # Page 4
        (7, 0, 0.00, 0.50, 0.5),  # Page 8
        (0, 0, 0.25, 0.50, 0.5),  # Page 1
        (1, 0, 0.50, 0.50, 0.5),  # Page 2
        (2, 0, 0.75, 0.50, 0.5),  # Page 3
    ]




    # Place each page in the appropriate position with rotation
    for page_idx, rotation, pos_x, pos_y, scale in page_layout:
        actual_page_idx = start_page + page_idx

        # Skip if the page doesn't exist in the input document
        if actual_page_idx - start_page >= 8:
            continue

        # Calculate position and size
        original_rect = doc[actual_page_idx].rect



        # Create a transformation matrix for positioning and scaling
        rect = fitz.Rect(
            page_size.width * pos_x,
            page_size.height * pos_y,
            page_size.width * pos_x + original_rect.width,
            page_size.height * pos_y + original_rect.height
        )

        # Apply the transformation (position, scale, and rotation)
        out_page.show_pdf_page(
            rect,
            doc,
            actual_page_idx,
            rotate=rotation
        )

    # Save the output document
    try:
        out_doc.save(output)
        print(f"Created pocketmod PDF: {output}")
        return True
    except Exception as e:
        click.echo(f"Error saving output PDF: {e}", err=True)
        return False
    finally:
        # Close both documents
        doc.close()
        out_doc.close()

@cli.command()
def version():
    """Show the current version."""
    click.echo("PDF 2 Pocketmod, version 0.1.0")

if __name__ == '__main__':
    cli()