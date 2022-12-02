# sudo service solr stop
# conda activate IR_Project
python schema_less_indexing.py CHITCHAT refined_cc_personality.json
sudo rm -rf /var/solr/data/CHITCHAT/conf/managed-schema.xml
# sudo cp solrconfig.xml /var/solr/data/Project3_BM25/conf/solrconfig.xml
sudo cp cc-schema.xml /var/solr/data/CHITCHAT/conf/schema.xml
sudo cp cmap.txt /var/solr/data/CHITCHAT/
# python schema_less_indexing.py Project3_BM25 index
curl "http://localhost:8001/solr/admin/cores?action=RELOAD&core=CHITCHAT"

python schema_less_indexing.py REDDIT refined_reddit.json
sudo rm -rf /var/solr/data/REDDIT/conf/managed-schema.xml
# sudo sudo cp /var/solr/data/Project3_VSM/conf/solrconfig.xml currentsolrconfig.xml
# sudo cp solrconfig.xml /var/solr/data/Project3_VSM/conf/solrconfig.xml
sudo cp reddit-schema.xml /var/solr/data/REDDIT/conf/schema.xml
sudo cp cmap.txt /var/solr/data/REDDIT/
curl "http://localhost:8001/solr/admin/cores?action=RELOAD&core=REDDIT"

