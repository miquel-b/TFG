import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


"""
Generates a manufacturing timeline chart for shareholder presentation.
"""
# 🎨 Define modern color palette
colors = {
    'Product A': '#A90533',   #Light Red 
    'Product B': '#103273',  # Light Blue
    'Product C': '#EE8976',  # Very Light Red
    'Complete Cleaning': '#737373', # Gray
    'Batch Change Over': '#BDBDBD', # Gray
}

conditioning_tasks = [
    ('Product A', 40, 'Product A'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product A', 50, 'Product A'),
    ('Complete Cleaning', 80 , 'Complete Cleaning'),
    ('Product B', 50, 'Product B'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product B', 20, 'Product B'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product B', 40, 'Product B'),
    ('Complete Cleaning', 80 , 'Complete Cleaning'),
    ('Product C', 30, 'Product C'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product C', 10, 'Product C'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product C', 20, 'Product C')
]


# 📊 Setup the plot
fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
ax.set_facecolor('white')

# Hide the y-axis spines and ticks for a cleaner look
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('none')
ax.yaxis.set_tick_params(pad=15) # Add padding for labels

# Remove x-axis grid lines
ax.xaxis.grid(False)
ax.set_xticks([])
# Define stage labels and their y-positions
stages = ['Jars Line \n (Conditioning and Packing)']
y_pos = [0]

current_time_conditioning = 0
for task_name, duration, category in conditioning_tasks:
    ax.barh(y_pos[0], duration, left=current_time_conditioning, color=colors[category],
            label=category,height=0.3)
    current_time_conditioning += duration
    '''
    if not (task_name=='Batch Change Over'):
        ax.text(current_time_conditioning - duration / 2, y_pos[2], 
                task_name,
                #task_name.replace('Product ', 'P '), 
                ha='center', va='center', color='black', fontsize=6, fontweight='bold')
'''
# Set y-axis labels
ax.set_yticks(y_pos)
ax.set_yticklabels(stages, fontsize=12)
ax.set_ylim(-0.5, 0.5)   # just enough space around the bar
# Set x-axis labels and title
ax.set_xlabel('Time', fontsize=12, labelpad=15)
ax.set_title('Manufacturing Process Timeline (Jars Line)', fontsize=16, fontweight='bold', pad=20)

# 🏷️ Create a custom legend to avoid duplicate labels
handles = [mpatches.Patch(color=colors['Product A'], label='Product A'),
           mpatches.Patch(color=colors['Product B'], label='Product B'),
           mpatches.Patch(color=colors['Product C'], label='Product C'),
           mpatches.Patch(color=colors['Batch Change Over'], label='Batch Change Over'),
           mpatches.Patch(color=colors['Complete Cleaning'], label='Complete Cleaning')]
ax.legend(handles=handles, loc='center',bbox_to_anchor=(0.5,-0.15),ncols=5)

plt.tight_layout()
plt.savefig('../Pictures/manufacturing_timeline_Jars_line.png', dpi=300)
plt.show()

