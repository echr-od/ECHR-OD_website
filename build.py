import os
import errno
from distutils.dir_util import copy_tree
from shutil import copy2

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

DATASETS_BUILD_PATH = '../echr-scraping/build/echr_database/'

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = "output"
PAGES_FOLDER = 'input/pages'

template_path = 'input/template'

INDEX = 'index.html'

TAGS = {
	'HEADER': 'header.html',
	'LEFT_COLUMN': 'left_column.html',
	'NAVIGATION': 'navigation.html',
	'FOOTER': 'footer.html'
}

PAGES = {
	'index': 'home.html',
	'explore': 'explore.html',
	'datasets': 'datasets.html',
	'about': 'about.html',
	'support': 'support.html'
}

ASSETS_FOLDERS = ['assets', 'css', 'fonts', 'js']

tags_content = dict(zip(TAGS.keys(), [None] * len(TAGS)))
for k in tags_content:
	with open(os.path.join(template_path, TAGS[k]), 'r') as f:
		tags_content[k] = f.read()
		f.close()


index_content = None
with open(os.path.join(template_path, INDEX), 'r') as f:
	index_content = f.read()
	f.close()

for k in tags_content.keys():
		index_content = index_content.replace("{" + k + "}", tags_content[k])

for page in PAGES:
	page_content = None
	with open(os.path.join(PAGES_FOLDER, PAGES[page]), 'r') as f:
		page_content = f.read()
		f.close()
	index_content_final = index_content.replace("{CONTENT}", page_content)
	output_path = os.path.join(OUTPUT_FOLDER, page, 'index.html')
	if page == 'index':
		output_path = os.path.join(OUTPUT_FOLDER, 'index.html')
	else:
		mkdir_p(os.path.join(OUTPUT_FOLDER, page))
	with open(output_path, 'w') as f:
		f.write(index_content_final)
		f.close()

for asset in ASSETS_FOLDERS:
	copy_tree(os.path.join(INPUT_FOLDER, asset), os.path.join(OUTPUT_FOLDER, asset))

d = os.path.join(DATASETS_BUILD_PATH, 'datasets_documents')

datasets_folders = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
for ds_folder in datasets_folders:
	ds_name = ds_folder.split('/')[-1]
	ds_output =  os.path.join(os.path.join(OUTPUT_FOLDER, 'assets/datasets_documents', ds_name))
	mkdir_p(ds_output)
	copy2(os.path.join(ds_folder, 'statistics_datasets.json'), ds_output)