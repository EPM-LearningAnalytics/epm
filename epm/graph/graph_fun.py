"""
"""

import altair as alt

def plot_log(data, y_option):
    """
    """
    p = alt.Chart(data, width=350, height=400).mark_bar().encode(
        x='session:N',
        y=y_option,
        color='activity',
        tooltip=[y_option, 'activity']
        ).interactive()
    
    return p

