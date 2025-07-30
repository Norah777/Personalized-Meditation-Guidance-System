package com.springboot.springbootlogindemo.controller;

import com.springboot.springbootlogindemo.domain.MoodLog;
import com.springboot.springbootlogindemo.service.MoodLogService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.time.LocalDate;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;


@RestController
@RequestMapping("/mood-logs")
public class MoodLogController {
    @Autowired
    private RestTemplate restTemplate;

    private static final Logger logger = LoggerFactory.getLogger(MoodLogController.class);

    private static final String VIDEO_DIR = "video";
    private static final String VIDEO_FILE_NAME = "test.mp4";
    private static final String FLASK_SERVICE_URL = "http://localhost:8008";

    @Resource
    private MoodLogService moodLogService;

    @PostMapping
    public ResponseEntity<?> createMoodLog(@RequestBody MoodLog moodLog) {
        try {
            MoodLog savedLog = moodLogService.saveMoodLog(moodLog);
            return ResponseEntity.ok(savedLog);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("保存情绪日志失败：" + e.getMessage());
        }
    }


    @GetMapping("/calendar")
    public ResponseEntity<?> getCalendarData(
            @RequestParam int userId,
            @RequestParam int year,
            @RequestParam int month) {
        Map<String, Object> calendarData = moodLogService.getCalendarData(userId, year, month);
        return ResponseEntity.ok(calendarData);
    }

    @GetMapping("/date")
    public ResponseEntity<?> getMoodLogByDate(
            @RequestParam String date,
            @RequestParam int userId) {
        try {
            MoodLog moodLog = moodLogService.getMoodLogByDate(userId, date);
            if (moodLog != null) {
                return ResponseEntity.ok(moodLog);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body("未找到该日期的情绪日志");
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("获取情绪日志失败：" + e.getMessage());
        }
    }

    @PostMapping("/startMeditation")
    public ResponseEntity<?> startMeditation(
            @RequestParam Integer userId,
            @RequestParam String mood,
            @RequestParam String content,
            @RequestParam String guideText,
            @RequestParam(value = "guideAudio", required = false) MultipartFile guideAudio,
            @RequestParam(value = "image", required = false) MultipartFile image,
            @RequestParam(required = false) String meditationType,
            @RequestParam(required = false) Integer duration
    ) throws IOException {
        MoodLog log = new MoodLog();
        log.setUserId(userId);
        log.setLogDate(LocalDate.now());
        log.setMood(mood);
        log.setContent(content);
        log.setGuideText(guideText);
        log.setMeditationType(meditationType);
        log.setDuration(duration);
        // 使用绝对路径保存文件
        String rootPath = System.getProperty("user.dir");
        String timeStamp = String.valueOf(System.currentTimeMillis());
        String basePath = rootPath + File.separator + "uploads" + File.separator + "moodlog" + File.separator + timeStamp;
        File dir = new File(basePath);
        if (!dir.exists()) dir.mkdirs();
        if (guideAudio != null && !guideAudio.isEmpty()) {
            String audioPath = basePath + File.separator + "guideAudio.mp3";
            guideAudio.transferTo(new File(audioPath));
            log.setGuideAudioUrl("/uploads/moodlog/" + timeStamp + "/guideAudio.mp3");
        }
        if (image != null && !image.isEmpty()) {
            String imagePath = basePath + File.separator + "image.png";
            image.transferTo(new File(imagePath));
            log.setImageUrl("/uploads/moodlog/" + timeStamp + "/image.png");
        }
        // 合成视频逻辑（伪实现）
        log.setVideoUrl("http://example.com/video/" + timeStamp + ".mp4");
        MoodLog saved = moodLogService.saveMoodLog(log);
        return ResponseEntity.ok(saved);
    }

    @PostMapping("/generateText")
    public ResponseEntity<?> generateText(
            @RequestParam Integer userId,
            @RequestParam String mood,
            @RequestParam String content
    ) {
        try {
            logger.info("开始生成文本，用户ID：{}，心情：{}，内容：{}", userId, mood, content);
            
            // 调用Flask服务生成文本
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("user_prompt", content);
            requestBody.put("emotional_state", mood);

            String url = FLASK_SERVICE_URL + "/generate-text";
            logger.info("调用Flask服务：{}", url);
            ResponseEntity<Map> response = restTemplate.postForEntity(url, requestBody, Map.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                Map<String, Object> responseBody = response.getBody();
                if (responseBody != null && responseBody.containsKey("success") && 
                    Boolean.TRUE.equals(responseBody.get("success"))) {
                    String generatedText = (String) responseBody.get("text");
                    logger.info("文本生成成功，长度：{}", generatedText.length());
                    return ResponseEntity.ok(Collections.singletonMap("text", generatedText));
                } else {
                    logger.error("Flask服务返回失败结果：{}", responseBody);
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body("Text generation failed: " + responseBody.get("message"));
                }
            } else {
                logger.error("Flask服务返回错误状态码：{}", response.getStatusCode());
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                        .body("Error from Flask service: " + response.getBody());
            }

        } catch (Exception e) {
            logger.error("生成文本失败", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("生成文本失败：" + e.getMessage());
        }
    }

    @PostMapping("/generateImage")
    public ResponseEntity<?> generateImage(
            @RequestParam Integer userId,
            @RequestParam String textContent,
            @RequestParam(required = false) String sessionId
    ) {
        try {
            logger.info("开始生成图片，用户ID：{}，文本内容长度：{}，会话ID：{}", userId, textContent.length(), sessionId);
            
            // 调用Flask服务生成图片
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("text_content", textContent);
            if (sessionId != null && !sessionId.isEmpty()) {
                requestBody.put("session_id", sessionId);
            }

            String url = FLASK_SERVICE_URL + "/generate-image";
            logger.info("调用Flask服务：{}", url);
            ResponseEntity<Map> response = restTemplate.postForEntity(url, requestBody, Map.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                Map<String, Object> responseBody = response.getBody();
                if (responseBody != null && responseBody.containsKey("success") && 
                    Boolean.TRUE.equals(responseBody.get("success"))) {
                    String originalImagePath = (String) responseBody.get("image_path");
                    String returnedSessionId = (String) responseBody.get("session_id");
                    logger.info("Flask服务返回的图片路径：{}，会话ID：{}", originalImagePath, returnedSessionId);
                    
                    if (originalImagePath != null && !originalImagePath.isEmpty()) {
                        // 检查图片是否已经在uploads目录中
                        File sourceFile = new File(originalImagePath);
                        if (sourceFile.exists()) {
                            // 检查路径是否包含uploads/images
                            if (originalImagePath.contains("uploads" + File.separator + "images")) {
                                // 文件已经在正确位置，提取从uploads开始的相对路径
                                int uploadsIndex = originalImagePath.indexOf("uploads");
                                String relativePath = originalImagePath.substring(uploadsIndex + "uploads".length());
                                // 确保路径以 / 开头
                                if (!relativePath.startsWith("/")) {
                                    relativePath = "/" + relativePath;
                                }
                                // 将文件分隔符统一为 /
                                relativePath = relativePath.replace(File.separator, "/");
                                String imageUrl = relativePath;
                                logger.info("图片已在uploads目录中，返回URL：{}", imageUrl);
                                
                                // 返回结果包含sessionId
                                Map<String, Object> result = new HashMap<>();
                                result.put("imageUrl", imageUrl);
                                result.put("sessionId", returnedSessionId);
                                return ResponseEntity.ok(result);
                            } else {
                                // 需要复制文件到uploads目录
                                String timestamp = String.valueOf(System.currentTimeMillis());
                                String imageFileName = "meditation_image_" + timestamp + ".png";
                                
                                // 获取uploads/images目录的绝对路径 - 修复路径配置
                                String uploadsPath = System.getProperty("user.dir") + File.separator + "uploads" + File.separator + "images" + File.separator;
                                File imageDir = new File(uploadsPath);
                                if (!imageDir.exists()) {
                                    imageDir.mkdirs();
                                    logger.info("创建图片目录：{}", uploadsPath);
                                }
                                
                                // 复制文件
                                File targetFile = new File(uploadsPath + imageFileName);
                                
                                logger.info("源文件路径：{}", sourceFile.getAbsolutePath());
                                logger.info("目标文件路径：{}", targetFile.getAbsolutePath());
                                
                                Files.copy(sourceFile.toPath(), targetFile.toPath(), 
                                        StandardCopyOption.REPLACE_EXISTING);
                                logger.info("图片文件复制完成");
                                
                                // 返回HTTP可访问的URL
                                String imageUrl = "/images/" + imageFileName;
                                logger.info("返回图片URL：{}", imageUrl);
                                
                                // 返回结果包含sessionId
                                Map<String, Object> result = new HashMap<>();
                                result.put("imageUrl", imageUrl);
                                result.put("sessionId", returnedSessionId);
                                return ResponseEntity.ok(result);
                            }
                        } else {
                            logger.error("源图片文件不存在：{}", originalImagePath);
                            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                    .body("Source image file not found");
                        }
                    } else {
                        logger.error("Flask服务返回空的图片路径");
                        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                .body("Flask service returned empty image path");
                    }
                } else {
                    logger.error("Flask服务返回失败结果：{}", responseBody);
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body("Image generation failed: " + responseBody.get("message"));
                }
            } else {
                logger.error("Flask服务返回错误状态码：{}", response.getStatusCode());
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                        .body("Error from Flask service: " + response.getBody());
            }

        } catch (Exception e) {
            logger.error("生成图片失败", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("生成图片失败：" + e.getMessage());
        }
    }

    @PostMapping("/generateVideoFromText")
    public ResponseEntity<?> generateVideoFromText(
            @RequestParam Integer userId,
            @RequestParam String textContent,
            @RequestParam(required = false) String imagePath,
            @RequestParam(required = false) String sessionId
    ) {
        try {
            logger.info("开始生成视频，用户ID：{}，文本内容长度：{}，图片路径：{}，会话ID：{}", userId, textContent.length(), imagePath, sessionId);
            
            // 调用Flask服务生成视频
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("text_content", textContent);
            if (imagePath != null && !imagePath.isEmpty()) {
                requestBody.put("image_path", imagePath);
            }
            if (sessionId != null && !sessionId.isEmpty()) {
                requestBody.put("session_id", sessionId);
            }

            String url = FLASK_SERVICE_URL + "/generate-video";
            logger.info("调用Flask服务：{}", url);
            ResponseEntity<Map> response = restTemplate.postForEntity(url, requestBody, Map.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                Map<String, Object> responseBody = response.getBody();
                if (responseBody != null && responseBody.containsKey("success") && 
                    Boolean.TRUE.equals(responseBody.get("success"))) {
                    String originalVideoPath = (String) responseBody.get("video_path");
                    String returnedSessionId = (String) responseBody.get("session_id");
                    logger.info("Flask服务返回的视频路径：{}，会话ID：{}", originalVideoPath, returnedSessionId);
                    
                    if (originalVideoPath != null && !originalVideoPath.isEmpty()) {
                        // 检查视频是否已经在uploads目录中
                        File sourceFile = new File(originalVideoPath);
                        if (sourceFile.exists()) {
                            // 检查路径是否包含uploads/videos
                            if (originalVideoPath.contains("uploads" + File.separator + "videos")) {
                                // 文件已经在正确位置，提取从uploads开始的相对路径
                                int uploadsIndex = originalVideoPath.indexOf("uploads");
                                String relativePath = originalVideoPath.substring(uploadsIndex + "uploads".length());
                                // 确保路径以 / 开头
                                if (!relativePath.startsWith("/")) {
                                    relativePath = "/" + relativePath;
                                }
                                // 将文件分隔符统一为 /
                                relativePath = relativePath.replace(File.separator, "/");
                                String videoUrl = relativePath;
                                logger.info("视频已在uploads目录中，返回URL：{}", videoUrl);
                                
                                // 返回结果包含sessionId
                                Map<String, Object> result = new HashMap<>();
                                result.put("videoUrl", videoUrl);
                                result.put("sessionId", returnedSessionId);
                                return ResponseEntity.ok(result);
                            } else {
                                // 需要复制文件到uploads目录
                                String timestamp = String.valueOf(System.currentTimeMillis());
                                String videoFileName = "meditation_video_" + timestamp + ".mp4";
                                
                                // 获取uploads/videos目录的绝对路径 - 修复路径配置
                                String uploadsPath = System.getProperty("user.dir") + File.separator + "uploads" + File.separator + "videos" + File.separator;
                                File videoDir = new File(uploadsPath);
                                if (!videoDir.exists()) {
                                    videoDir.mkdirs();
                                    logger.info("创建视频目录：{}", uploadsPath);
                                }
                                
                                // 复制文件
                                File targetFile = new File(uploadsPath + videoFileName);
                                
                                logger.info("源文件路径：{}", sourceFile.getAbsolutePath());
                                logger.info("目标文件路径：{}", targetFile.getAbsolutePath());
                                
                                Files.copy(sourceFile.toPath(), targetFile.toPath(), 
                                        StandardCopyOption.REPLACE_EXISTING);
                                logger.info("视频文件复制完成");
                                
                                // 返回HTTP可访问的URL
                                String videoUrl = "/videos/" + videoFileName;
                                logger.info("返回视频URL：{}", videoUrl);
                                
                                // 返回结果包含sessionId
                                Map<String, Object> result = new HashMap<>();
                                result.put("videoUrl", videoUrl);
                                result.put("sessionId", returnedSessionId);
                                return ResponseEntity.ok(result);
                            }
                        } else {
                            logger.error("源视频文件不存在：{}", originalVideoPath);
                            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                    .body("Source video file not found");
                        }
                    } else {
                        logger.error("Flask服务返回空的视频路径");
                        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                .body("Flask service returned empty video path");
                    }
                } else {
                    logger.error("Flask服务返回失败结果：{}", responseBody);
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body("Video generation failed: " + responseBody.get("message"));
                }
            } else {
                logger.error("Flask服务返回错误状态码：{}", response.getStatusCode());
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                        .body("Error from Flask service: " + response.getBody());
            }

        } catch (Exception e) {
            logger.error("生成视频失败", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("生成视频失败：" + e.getMessage());
        }
    }

    @PostMapping("/generateVideo")
    public ResponseEntity<?> generateVideo(
            @RequestParam Integer userId,
            @RequestParam String mood,
            @RequestParam String content
    ) {
        try {
            logger.info("开始生成视频，用户ID：{}，心情：{}，内容：{}", userId, mood, content);
            
            // 调用Flask服务生成视频
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("user_prompt", content);
            requestBody.put("emotional_state", mood);

            String url = "http://localhost:8008/process";
            RestTemplate restTemplate = new RestTemplate();
            logger.info("调用Flask服务：{}", url);
            ResponseEntity<Map> response = restTemplate.postForEntity(url, requestBody, Map.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                Map<String, Object> responseBody = response.getBody();
                String originalVideoPath = responseBody != null ? (String) responseBody.get("video_path") : "";
                logger.info("Flask服务返回的视频路径：{}", originalVideoPath);
                
                if (originalVideoPath != null && !originalVideoPath.isEmpty()) {
                    // 复制视频文件到Spring Boot的静态资源目录
                    String timestamp = String.valueOf(System.currentTimeMillis());
                    String videoFileName = "meditation_" + timestamp + ".mp4";
                    
                    // 获取uploads/videos目录的绝对路径 - 修复路径配置
                    String uploadsPath = System.getProperty("user.dir") + File.separator + "uploads" + File.separator + "videos" + File.separator;
                    File videoDir = new File(uploadsPath);
                    if (!videoDir.exists()) {
                        videoDir.mkdirs();
                        logger.info("创建视频目录：{}", uploadsPath);
                    }
                    
                    // 复制文件
                    File sourceFile = new File(originalVideoPath);
                    File targetFile = new File(uploadsPath + videoFileName);
                    
                    logger.info("源文件路径：{}", sourceFile.getAbsolutePath());
                    logger.info("目标文件路径：{}", targetFile.getAbsolutePath());
                    logger.info("源文件是否存在：{}", sourceFile.exists());
                    
                    Files.copy(sourceFile.toPath(), targetFile.toPath(), 
                            StandardCopyOption.REPLACE_EXISTING);
                    
                    logger.info("文件复制完成，目标文件是否存在：{}", targetFile.exists());
                    logger.info("目标文件大小：{} bytes", targetFile.length());
                    
                    // 返回HTTP可访问的URL
                    String videoUrl = "/videos/" + videoFileName;
                    logger.info("返回视频URL：{}", videoUrl);
                    return ResponseEntity.ok(Collections.singletonMap("videoUrl", videoUrl));
                } else {
                    logger.error("Flask服务返回空的视频路径");
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body("Flask service returned empty video path");
                }
            } else {
                logger.error("Flask服务返回错误状态码：{}", response.getStatusCode());
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                        .body("Error from Flask service: " + response.getBody());
            }

        } catch (Exception e) {
            logger.error("获取视频失败", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("获取视频失败：" + e.getMessage());
        }
    }

}
