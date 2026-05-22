.PHONY: setup pipeline dashboard

setup:
	sudo apt install -y wkhtmltopdf
	pip install -r requirements.txt
	python3 load_data.py

pipeline:
	python3 pipeline.py

dashboard:
	streamlit run dashboard.py