package co.mega.mars.ndata.controller;

import co.mega.mars.ndata.service.MqttService;
import co.mega.mars.ndata.service.VehicleLogService;
import lombok.Builder;
import lombok.ToString;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.text.SimpleDateFormat;
import java.util.*;

import java.io.*;

@Slf4j
@Controller
public class VehLogController {

    @Autowired
    VehicleLogService vehicleLogService;
    @Autowired
    MqttService mqttService;
    @Value("${veh.log.path}")
    String vehLogPath;
    @Value("${veh.log.url.prefix}")
    String logFilePrefix;

    @GetMapping("/vehlog/vids")
    public ResponseEntity<Object> getVidList(){
        Set<String> vids = new HashSet<>();
        File root = new File(vehLogPath);
        for(File datePath : root.listFiles()) {
            if (!datePath.isDirectory()) continue;
            log.info("dataPath {}", datePath);
            for (File vidPath : datePath.listFiles()) {
                if (vidPath.isDirectory() && vidPath.getName().length() == 32) {
                    vids.add(vidPath.getName());
                }
            }
        }
        return new ResponseEntity<Object>(RestResult.getSuccessResult(vids), HttpStatus.OK);
    }

    public List<VehLog> searchLogs(String vid){
        List<VehLog> logs = new ArrayList<>();

        File root = new File(vehLogPath);
        for(File datePath : root.listFiles()){
            if( ! datePath.isDirectory())continue;
            log.info("dataPath {}",datePath);
            for(File vidPath : datePath.listFiles()){
                if( vidPath.isDirectory() && vid.equalsIgnoreCase(vidPath.getName())){
                    File p = new File(vidPath.getAbsolutePath()+"/0/");

                    Map<String,List<LogFile>> logByDate = new HashMap<>();
                    for(File logFile : p.listFiles()){
                        String n = logFile.getName();
                        if( n.startsWith("."))continue;
                        LogFile l = new LogFile(n,logFilePrefix + datePath.getName() + "/" + vidPath.getName() + "/0/" + n);
                        log.info("log file : {}", n);
                        if( n.length() < 18)continue;
                        String createdAt = n.substring(8,18);
                        List<LogFile> ls = logByDate.get(createdAt);
                        if( ls == null){
                            ls = new ArrayList<>();
                            logByDate.put(createdAt, ls);
                        }
                        ls.add(l);
                    }

                    for(Map.Entry<String,List<LogFile>> ett : logByDate.entrySet()){
                        VehLog log = new VehLog();
                        log.uploadedAt = datePath.getName();
                        log.createdAt = ett.getKey();
                        log.files = ett.getValue();

                        logs.add(log);
                    }
                }
            }
        }
        return logs;
    }

    @GetMapping("/vehlog/searchLog")
    public ResponseEntity<Object> searchLog(String vid){
        return new ResponseEntity<Object>(RestResult.getSuccessResult(searchLogs(vid)), HttpStatus.OK);
    }

    @PostMapping("/vehlog/requestLog")
    public ResponseEntity<Object> requestLog(@RequestBody RequestLogForm form){
        log.info("requst log : {}",form);
        try {
            SimpleDateFormat parser = new SimpleDateFormat("yyyy-MM-dd HH:mm");
            Date date = parser.parse(form.startTs);

            mqttService.sendUploadLogMsg(form.vid, date.getTime(), form.hourCount);
        }catch (Exception ex){
            log.error("Failed to request vehicle log for {}", form, ex);
            return new ResponseEntity<Object>(RestResult.getFailResult(ex.getMessage(),null), HttpStatus.OK);
        }
        return new ResponseEntity<Object>(RestResult.getSuccessResult(), HttpStatus.OK);
    }

    static class VehLog{
        public String uploadedAt;
        public String createdAt;
        public List<LogFile> files;
    }

    @Builder
    static class LogFile{
        public String name;
        public String link;
    }

    @ToString
    static class RequestLogForm {
        public String vid;
        public String startTs;
        public int hourCount;
    }
}
