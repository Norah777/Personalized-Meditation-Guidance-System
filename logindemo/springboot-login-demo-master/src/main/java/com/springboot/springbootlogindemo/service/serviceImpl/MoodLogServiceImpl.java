package com.springboot.springbootlogindemo.service.serviceImpl;

import com.springboot.springbootlogindemo.domain.MoodLog;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import com.springboot.springbootlogindemo.repository.MoodLogDao;
import com.springboot.springbootlogindemo.service.MoodLogService;

import javax.annotation.Resource;

@Service
public class MoodLogServiceImpl implements MoodLogService {

    @Resource
    private MoodLogDao moodLogDao;

    @Override
    public MoodLog saveMoodLog(MoodLog moodLog) {
        // 检查是否已经存在当天的记录
        MoodLog existingLog = moodLogDao.findByUserIdAndLogDate(
            moodLog.getUserId(), moodLog.getLogDate());
        
        if (existingLog != null) {
            // 设置已有记录的ID，保存时会执行更新而不是插入
            moodLog.setId(existingLog.getId());
        }
        
        return moodLogDao.save(moodLog);
    }



    @Override
    public Map<String, Object> getCalendarData(int userId, int year, int month) {
        List<MoodLog> logs = moodLogDao.findByUserId(userId);
        Map<String, Object> calendarData = new HashMap<>();

        // 构造这个月的起止日期
        LocalDate start = LocalDate.of(year, month, 1);
        LocalDate end = start.withDayOfMonth(start.lengthOfMonth());

        // 过滤该月的日志数据
        List<Map<String, Object>> days = logs.stream()
                .filter(log -> {
                    LocalDate date = log.getLogDate(); // 确保 logDate 是 LocalDate 类型
                    return !date.isBefore(start) && !date.isAfter(end);
                })
                .map(log -> {
                    Map<String, Object> day = new HashMap<>();
                    day.put("date", log.getLogDate().toString()); // 格式为 yyyy-MM-dd
                    day.put("mood", log.getMood());
                    return day;
                })
                .collect(Collectors.toList());

        calendarData.put("days", days);
        return calendarData;
    }


    @Override
    public MoodLog getMoodLogByDate(int userId, String date) {
        LocalDate logDate = LocalDate.parse(date);
        return moodLogDao.findByUserIdAndLogDate(userId, logDate);
    }
}
