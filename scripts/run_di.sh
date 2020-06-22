while true; do
	python3 sync_wakeup_wav.py 3
	python3 sync_ri_v2.py 3
	python3 vos_ri.py 3
	sleep 60
done
