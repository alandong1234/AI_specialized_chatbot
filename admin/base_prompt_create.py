import numpy as np
x = np.array([{'role': 'system', 'content': 'You are an Artificial Intelligent.'}])
np.save('admin_prompt', x)