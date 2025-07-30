package com.springboot.springbootlogindemo.repository;

import com.springboot.springbootlogindemo.domain.MoodLog;
import org.springframework.data.jpa.repository.JpaRepository;
import java.time.LocalDate;
import java.util.Date;
import java.util.List;

public interface MoodLogDao extends JpaRepository<MoodLog, Integer> {
    MoodLog findByUserIdAndLogDate(Integer userId, LocalDate logDate);
    List<MoodLog> findByUserId(Integer userId);
    List<MoodLog> findByUserIdAndLogDateBetween(Integer userId, Date startDate, Date endDate);

}
