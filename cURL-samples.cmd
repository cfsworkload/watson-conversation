Q-and-A/service/ - POST
curl -X POST -H "Content-Type:application/json" -d "{\"question\":\"Can I get a degree in HCA?\", \"client_id\":\"156008\", \"conversation_id\":\"164662\"}" "http://localhost:5000/service/"

R-and-R - Create SOLR cluster
curl -k -X POST -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters" -d "" 

R-and-R - Check status of SOLR cluster
curl -k -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d"

R-and-R - Upload sample SOLR config file
curl -k -X POST -H "Content-Type: application/zip" -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d/config/example-config" --data-binary @pmi_solr_config.zip

R-and-R - Create collection 'example-collection'
curl -k -X POST -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d/solr/admin/collections" -d "action=CREATE&name=example-collection&collection.configName=example-config"

R-and-R Add documents
curl -k -X POST -H "Content-Type: application/json" -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d/solr/example-collection/update" --data-binary @pmi_data.json

R-and-R Delete SOLR cluster
curl -k -X DELETE -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d"

R-and-R Delete Ranker
curl -k -X DELETE -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/rankers/F3551Dx1-rank-340"

R-and-R Python script to create Ranker
c:\python27\python train.py -u a29d38a4-328a-4d72-89ec-a029e730e6e3:UuI5HXPrepLr -i pmi_gt.csv -c sc136d46ca_57a5_4c99_8745_70ee1733683d -x example-collection -n "example-ranker"

R-and-R Retrieve status of ranker
curl -k -u "a29d38a4-328a-4d72-89ec-a029e730e6e3":"UuI5HXPrepLr"  "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/rankers/F3551Dx1-rank-341"

R-and-R Retrieve search results
https://a29d38a4-328a-4d72-89ec-a029e730e6e3:UuI5HXPrepLr@gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d/solr/example-collection/select?q=what is the basic mechanism of the transonic aileron buzz&wt=json&fl=id,title

R-and-R Retrieve reranked results
https://a29d38a4-328a-4d72-89ec-a029e730e6e3:UuI5HXPrepLr@gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc136d46ca_57a5_4c99_8745_70ee1733683d/solr/example-collection/fcselect?ranker_id=F3551Dx1-rank-344&q=prepare&nbsp;me&nbsp;for&nbsp;management&wt=json&fl=id,program,description