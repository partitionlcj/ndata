package co.mega.mars.ndata.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Service;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

@Service
public class BackendTaskService implements ApplicationListener<ApplicationReadyEvent> {

    @Autowired
    VehicleLogService vehicleLogService;

    @Override
    public void onApplicationEvent(ApplicationReadyEvent applicationReadyEvent) {
        ScheduledExecutorService ses = Executors.newScheduledThreadPool(1);
        ses.scheduleAtFixedRate(() -> {
            vehicleLogService.syncLogFiles();
        }, 30, 60, TimeUnit.SECONDS);
    }
}
