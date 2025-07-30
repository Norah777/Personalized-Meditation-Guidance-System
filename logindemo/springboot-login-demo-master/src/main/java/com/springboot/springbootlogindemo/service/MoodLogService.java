package com.springboot.springbootlogindemo.service;

import com.springboot.springbootlogindemo.domain.MoodLog;
import java.util.Map;

public interface MoodLogService {
    MoodLog saveMoodLog(MoodLog moodLog);
    Map<String, Object> getCalendarData(int userId, int year, int month);

    MoodLog getMoodLogByDate(int userId, String date);
}
