default: inprogress

inprogress:
	echo "Work in progress"

mongo:
	podman run --name mongomgr -d -v mongomgr:/data/db/ -p 27017:27017 mongo:4

mongocli:
	podman exec -i -t mongomgr mongo mgr

mongoexport:
	mongoexport --uri=mongodb://localhost:27017/mgr --collection playedtracks --out playedtracks.json

mongo_getlast:
	podman exec -i -t mongomgr mongo mgr  --eval 'db.playedtracks.find().sort({ "$$natural": -1}).limit(1)'