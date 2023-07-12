import streamlit as st
import importlib
import ast
import pandas as pd

# CC - Wrapper for checking and plotting the function.
def check_if_display_plot(ai_content, i):

    # PJ - remove first and last lines (which are triple quotes)
    if '```python' in ai_content:
        cut_length=10
    else:
        cut_length=3
        
    ai_content=ai_content[ai_content.find('```\n')+cut_length:ai_content.rfind('\n')]
    print("-"*80)
    print(ai_content)
    print("-"*80)

    if is_valid_python(ai_content):
        ai_content = "\n".join([f"    {line}" for line in ai_content.split("\n")])
        print(ai_content)
        plot_func_str = f"""\ndef plot_code(df):\n{ai_content}\n    return fig\n"""

        with open(f"plt_tmp{i}.py", 'w') as f:
            f.write(plot_func_str)

        print("Valid python - about to load plot.")
        plot_module = importlib.import_module(f"plt_tmp{i}")
        importlib.reload(plot_module)

        df = pd.read_csv("data/combined.csv")
        fig = plot_module.plot_code(df)
        display_plot(st, fig)

        print("\nDEBUG: Should have plotted.")
    else:
        print("\nDEBUG: Empty or invalid python - didn't plot anything.")


# CC - Display the plot with a few options.
def display_plot(st, fig):
    try:
        print("Plot 1")
        st.pyplot(fig.figure)
    except:
        try:
            print("Plot 2")
            st.pyplot(fig.figure_)
        except:
            print("Plot 3")
            st.pyplot(fig)

# PJ - function to check for valid python code
def is_valid_python(code):
   if code.strip() == "":
       return False
   try:
       ast.parse(code)
   except SyntaxError as e:
       #print(e)
       return False
   return True