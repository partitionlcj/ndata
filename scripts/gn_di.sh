while true; do
        python3 sync_ri_gn.py
        python3 sync_wakeup_gn.py
        python3 gn_report.py
        sleep 60
done
