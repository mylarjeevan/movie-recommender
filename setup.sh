mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml

pip install gdown

gdown --id 1WpbEOzHIVUuEjOLDSov4VDKxzWlvBbB4 -O similarity.pkl