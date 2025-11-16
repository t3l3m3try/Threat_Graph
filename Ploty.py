import pandas as pd
import plotly.express as px
import argparse
import sys
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create an interactive threat actor analysis chart from a CSV file.')
    parser.add_argument('input_csv', help='Path to the input CSV file')
    parser.add_argument('-o', '--output', help='Path to the output HTML file (default: same name as input with .html extension)')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.isfile(args.input_csv):
        print(f"Error: Input file '{args.input_csv}' not found.")
        sys.exit(1)
    
    # Determine output file path
    if args.output:
        output_file = args.output
    else:
        output_file = os.path.splitext(args.input_csv)[0] + '.html'
    
    # Read the CSV file with semicolon delimiter
    try:
        df = pd.read_csv(args.input_csv, sep=';')
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    # Strip whitespace from column names FIRST
    df.columns = df.columns.str.strip()
    
    # Validate required columns
    required_columns = ['Threat Actor', 'Impact', 'Sophistication', 'Hits']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Error: Missing required columns: {', '.join(missing_columns)}")
        print(f"Found columns: {', '.join(df.columns.tolist())}")
        sys.exit(1)
    
    # Strip whitespace from threat actor values
    df['Threat Actor'] = df['Threat Actor'].str.strip()
    
    # Create a Plotly scatter plot with increased circle size and more vivid colors
    fig = px.scatter(
        df, 
        x='Sophistication', 
        y='Impact', 
        size='Hits', 
        color='Threat Actor',
        hover_name='Threat Actor',
        title='Threat Actor Analysis: Impact vs Sophistication',
        labels={'Sophistication': 'Sophistication (Low to High)', 'Impact': 'Impact (Low to High)'},
        template='plotly_dark',  # Using a dark template for the cyberpunk look
        size_max=50,  # Increase the maximum bubble size to make circles more prominent
        opacity=1.0   # Adjust opacity to make colors more vivid
    )
    
    # Customize the layout for a more "cyberpunk" style without the grid or legend
    fig.update_layout(
        font_family="Courier New",
        font_color="cyan",
        title_font_family="Courier New",
        title_font_color="magenta",
        legend_title_font_color="lightblue",
        paper_bgcolor="black",
        plot_bgcolor="black",
        title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        showlegend=False,  # Remove the legend
        xaxis=dict(
            showgrid=False,  # Remove the grid
            zeroline=True,   # Show the x-axis line
            linecolor='cyan',  # Set the x-axis line color
        ),
        yaxis=dict(
            showgrid=False,  # Remove the grid
            zeroline=True,   # Show the y-axis line
            linecolor='cyan',  # Set the y-axis line color
        )
    )
    
    # Save the figure to an HTML file
    try:
        fig.write_html(output_file)
        print(f"✓ Interactive chart successfully created: {output_file}")
        print(f"✓ Processed {len(df)} threat actors")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
