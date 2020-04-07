package co.mega.mars.ndata.service;

import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import org.fusesource.mqtt.client.*;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
public class MqttService {


    private static final char MULTI_KEY_SEPARATOR = ((char) 7);

    private String getTopic(String appId, String deviceId) {
        return appId + MULTI_KEY_SEPARATOR + deviceId;
    }

    public MqttConfig getConfig(String env){
        if( "test".equalsIgnoreCase(env)) {
            MqttConfig test = new MqttConfig();
            test.url = "ssl://xmars-test.x-tetris.com:20191";
            test.user = "mars_admin";
            test.password = "!@#QWEasd456";
            return test;
        }
        else if ( "stg".equalsIgnoreCase(env)){
            MqttConfig stg = new MqttConfig();
            stg.url = "ssl://xmars-stg.x-tetris.com:20191";
            stg.user = "mars_admin";
            stg.password = "(OL>0p;/123QWE";
            return stg;
        }
        else if ( "prod".equalsIgnoreCase(env)){
            MqttConfig stg = new MqttConfig();
            stg.url = "ssl://xmars.x-tetris.com:20191";
            stg.user = "mars_admin";
            stg.password = "(OL>0p;/123QWE";
            return stg;
        }
        return null;
    }

    public void sendUploadLogMsg(String env, String appId, String vid, long startTime, int hourCount) throws Exception{
        MqttConfig cfg = getConfig(env);
        MQTT mqtt = new MQTT();
        mqtt.setHost(cfg.url);
        mqtt.setUserName(cfg.user);
        mqtt.setPassword(cfg.password);
        BlockingConnection connection = mqtt.blockingConnection();
        connection.connect();

        String topic = getTopic(appId,vid);

        Topic[] topics = {new Topic(topic, QoS.AT_LEAST_ONCE)};
        byte[] qoses = connection.subscribe(topics);

        Gson gson = new Gson();

        MessageContent messageContent = new MessageContent();
        messageContent.operations = new ArrayList();
        Operation operation = new Operation("uploadLog");

        operation.params.put("startTime", startTime);
        operation.params.put("hourCount", hourCount);
        messageContent.operations.add(operation);
        NotificationMessage notificationMessage = new NotificationMessage();
        notificationMessage.type = 0;
        notificationMessage.message = gson.toJson(messageContent);
        String pushMessage = gson.toJson(notificationMessage);
        connection.publish(topic, pushMessage.getBytes(), QoS.AT_LEAST_ONCE, false);

        Message message = connection.receive();
        log.info("message topic '{}',data {}",message.getTopic(), new String(message.getPayload(), "UTF-8"));

        String rt = new String(message.getPayload(), "UTF-8");
        log.info("notificationMessage {}",rt);
        message.ack();

        connection.disconnect();
    }

    static class MqttConfig{
        String url;
        String user;
        String password;
    }

    static class MessageContent {
        public List<OutputText> tts;

        public List<OutputText> viewText;

        public List<Operation> operations;
    }

    static class NotificationMessage {
        public int type;

        public String message;
    }

    static class OutputText {
        public String content;
    }

    static class Operation {
        public Operation(String type){
            this.type = type;
        }
        String type;
        Map<String, Object> params = new HashMap<>();
    }

}
