package co.mega.mars.ndata.service;

import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import org.fusesource.mqtt.client.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
public class MqttService {

    @Value("${mqtt.url}")
    String mqttURL = "ssl://xmars-test.x-tetris.com:20191";

    public void sendUploadLogMsg(String vid, long startTime, int hourCount) throws Exception{
        MQTT mqtt = new MQTT();
        mqtt.setHost(mqttURL);
        BlockingConnection connection = mqtt.blockingConnection();
        connection.connect();


        Topic[] topics = {new Topic(vid, QoS.AT_LEAST_ONCE)};
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
        connection.publish(vid, pushMessage.getBytes(), QoS.AT_LEAST_ONCE, false);

        Message message = connection.receive();
        log.info("message topic '{}',data {}",message.getTopic(), new String(message.getPayload(), "UTF-8"));

        String rt = new String(message.getPayload(), "UTF-8");
        log.info("notificationMessage {}",rt);
        message.ack();
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
