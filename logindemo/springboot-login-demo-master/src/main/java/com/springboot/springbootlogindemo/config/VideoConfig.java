package com.springboot.springbootlogindemo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.io.File;

@Configuration
public class VideoConfig implements WebMvcConfigurer {

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        // 创建视频文件存储目录
        String videoPath = System.getProperty("user.dir") + File.separator + "uploads" + File.separator + "videos" + File.separator;
        File videoDir = new File(videoPath);
        if (!videoDir.exists()) {
            videoDir.mkdirs();
        }
        
        // 添加静态资源映射
        registry.addResourceHandler("/videos/**")
                .addResourceLocations("file:" + videoPath);
    }
} 