package co.mega.mars.ndata.controller;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class DateUtil {
    public static final Long ONE_DAY_IN_MILLISECOND = 1L * 24 * 60 * 60 * 1000;

    private static final ThreadLocal<Calendar> threadLocal = ThreadLocal.withInitial(()->Calendar.getInstance());
    private static final ThreadLocal<DateFormat> dateFormatThreadLocal = ThreadLocal.withInitial(()->new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));
    private static final ThreadLocal<DateFormat>dayFormatThreadLocal = ThreadLocal.withInitial(()->new SimpleDateFormat("yyyyMMdd"));

    public static long getMillisecond(Calendar calendar) {
        return calendar.getTimeInMillis();
    }

    public static long getMillisecond(String date) {
        String[] arr = date.split("-");
        Calendar calendar = threadLocal.get();

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
        return dateFormatThreadLocal.get().format(new Date(millisecond));
    }

    public static long parseMillisecond(String date) throws Exception {
        return dateFormatThreadLocal.get().parse(date).getTime();
    }

    public static String dayFormat() throws Exception {
        return dayFormatThreadLocal.get().format(new Date());
    }
}
