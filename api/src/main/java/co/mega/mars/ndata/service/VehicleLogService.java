package co.mega.mars.ndata.service;

import com.google.common.base.Strings;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

import java.lang.reflect.Type;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
public class VehicleLogService {

    static Type listOfString = new TypeToken<ArrayList<String>>() {}.getType();

    VehLogRowMapper rowMapper = new VehLogRowMapper();

    @Autowired
    JdbcTemplate jdbcTemplate;

    public List<VehLog> getHisLogs(String vid){
        List<VehLog> result = jdbcTemplate.query("select * from vehicle_log where vehicle_id=?", new Object[]{vid}, rowMapper);
        return result;
    }

    static class VehLog{
        public Long id;
        public String vehicleId;
        public Long startTime;
        public int hourCount;
        public Date createdAt;
        public List<String> logFiles;
        public boolean fileSynced;
    }

    static class VehLogRowMapper implements RowMapper<VehLog> {

        Gson gson = new Gson();

        @Override
        public VehLog mapRow(ResultSet rs, int i) throws SQLException {
            VehLog l = new VehLog();
            l.id = rs.getLong("id");
            l.vehicleId = rs.getString("vehicle_id");
            l.startTime = rs.getLong("start_time");
            l.hourCount = rs.getInt("hour_count");
            l.createdAt = rs.getDate("created_at");

            int b = rs.getInt("file_synced");
            l.fileSynced = b > 0;

            String src = rs.getString("log_files");
            if( ! Strings.isNullOrEmpty(src)){
                l.logFiles = gson.fromJson(src, listOfString);
            }
            return l;
        }
    }
}
