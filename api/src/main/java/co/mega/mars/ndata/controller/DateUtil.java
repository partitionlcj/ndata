package co.mega.mars.ndata.controller;

import java.util.Calendar;
import java.util.TimeZone;

public class DateUtil {
    public static final Long ONE_DAY_IN_MILLISECOND = 1L * 24 * 60 * 60 * 1000;

    public static long getMillisecond(Calendar calendar) {
        return calendar.getTimeInMillis();
    }

    public static long getMillisecond(String date) {
        String[] arr = date.split("-");
        Calendar calendar = Calendar.getInstance();

        calendar.set(Calendar.YEAR, Integer.parseInt(arr[0]));
        calendar.set(Calendar.MONTH, Integer.parseInt(arr[1]) - 1);
        calendar.set(Calendar.DAY_OF_MONTH, Integer.parseInt(arr[2]));

        calendar.set(Calendar.HOUR_OF_DAY, 0);
        calendar.set(Calendar.MINUTE, 0);
        calendar.set(Calendar.SECOND, 0);

        return getMillisecond(calendar);
    }

    public static long getNextDayInMillisecond(String date) {
        return getMillisecond(date) + ONE_DAY_IN_MILLISECOND;
    }

    public static String formatDate(long millisecond) {
        Calendar c = Calendar.getInstance(TimeZone.getTimeZone("GMT-5"));
        c.setTimeInMillis(millisecond);
        StringBuilder sb = new StringBuilder();

        sb.append(c.get(Calendar.YEAR)).append("-").append(c.get(Calendar.MONTH)+1).append("-").append(c.get(Calendar.DAY_OF_MONTH))
                .append(" ").append(c.get(Calendar.HOUR_OF_DAY)).append(":").append(c.get(Calendar.MINUTE)).append(":").append(c.get(Calendar.SECOND));
        return sb.toString();
    }

}
