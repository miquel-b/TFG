import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


"""
Generates a manufacturing timeline chart for shareholder presentation.
"""
# 🎨 Define modern color palette
colors = {
    'Product A': '#E94840',   #Light Red 
    'Product B': '#00A3C2',  # Light Blue
    'Product C': '#EE8976',  # Very Light Red
    'Complete Cleaning': '#737373', # Gray
    'Batch Change Over': '#BDBDBD', # Gray
}

# ⚙️ Define manufacturing process data
# Each tuple is (task_name, duration, category)
raw_materials_tasks = [
    ('Product A', 30, 'Product A'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product A', 40, 'Product A'),
    ('Complete Cleaning', 25 , 'Complete Cleaning'),
    ('Product B', 30, 'Product B'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product B', 15, 'Product B'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product B', 28, 'Product B'),
    ('Complete Cleaning', 25 , 'Complete Cleaning'),
    ('Product C', 30, 'Product C'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product C', 20, 'Product C'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product C', 20, 'Product C')
]


# Calculate start times for each stage to ensure staggering
raw_materials_end_time =  25

compression_tasks = [
    ('Product A', 40, 'Product A'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product A', 40, 'Product A'),
    ('Complete Cleaning', 20 , 'Complete Cleaning'),
    ('Product B', 30, 'Product B'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product B', 10, 'Product B'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product B', 40, 'Product B'),
    ('Complete Cleaning', 20 , 'Complete Cleaning'),
    ('Product C', 30, 'Product C'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product C', 10, 'Product C'),
    ('Batch Change Over', 3, 'Batch Change Over'),
    ('Product C', 20, 'Product C')
]

compression_end_time = 50

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
stages = ['Raw Materials Handling', 'Compression', 'Conditioning and Packaging']
y_pos = [2, 1, 0]

# ✍️ Plot the bars for each stage
current_time_raw_materials = 0
for task_name, duration, category in raw_materials_tasks:
    ax.barh(y_pos[0], duration, left=current_time_raw_materials, color=colors[category],
            label=category, height=0.6)
    current_time_raw_materials += duration
        # Add text labels for each task
    '''
    if not (task_name=='Batch Change Over' or task_name=='Complete Cleaning'):
        ax.text(current_time_raw_materials - duration / 2, y_pos[0], 
                task_name,
                #task_name.replace('Product ', 'P'), 
                ha='center', va='center', color='black', fontsize=6, fontweight='bold')
'''

current_time_compression = raw_materials_end_time
for task_name, duration, category in compression_tasks:
    ax.barh(y_pos[1], duration, left=current_time_compression, color=colors[category],
            label=category, height=0.6)
    current_time_compression += duration
    '''
    if not (task_name=='Batch Change Over'):
        ax.text(current_time_compression - duration / 2, y_pos[1], 
                task_name,
                #task_name.replace('Product ', 'P'), 
                ha='center', va='center', color='black', fontsize=6, fontweight='bold')
'''

current_time_conditioning = compression_end_time
for task_name, duration, category in conditioning_tasks:
    ax.barh(y_pos[2], duration, left=current_time_conditioning, color=colors[category],
            label=category, height=0.6)
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

# Set x-axis labels and title
ax.set_xlabel('Time', fontsize=12, labelpad=15)
ax.set_title('Manufacturing Process Timeline', fontsize=16, fontweight='bold', pad=20)

# 🏷️ Create a custom legend to avoid duplicate labels
handles = [mpatches.Patch(color=colors['Product A'], label='Product A'),
           mpatches.Patch(color=colors['Product B'], label='Product B'),
           mpatches.Patch(color=colors['Product C'], label='Product C'),
           mpatches.Patch(color=colors['Batch Change Over'], label='Batch Change Over'),
           mpatches.Patch(color=colors['Complete Cleaning'], label='Complete Cleaning')]
ax.legend(handles=handles, loc='upper right', ncol=4, bbox_to_anchor=(1, 1.15))

plt.tight_layout()
plt.savefig('manufacturing_timeline.png', dpi=300)
plt.show()

