#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os
from urllib.error import HTTPError

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="vue-login-demo-master/dist", **kwargs)

    def do_POST(self):
        """Handle POST requests, proxy to backend API"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        """Handle GET requests, prioritize API, otherwise handle static files"""
        print(f"GET request: {self.path}")
        if self.path.startswith('/api/'):
            print("Handling API request")
            self.handle_api_request()
        elif self.path.startswith('/videos/'):
            print("Handling video request")
            self.handle_video_request()
        elif self.path.startswith('/images/'):
            print("Handling image request")
            self.handle_image_request()
        else:
            print("Handling static file request")
            # Check if it's a static file with extension
            if '.' in os.path.basename(self.path):
                # Handle static files (js, css, images, etc.)
                super().do_GET()
            else:
                # Handle Vue Router routes - return index.html for SPA
                print("Handling Vue Router route, returning index.html")
                self.path = '/index.html'
                super().do_GET()

    def do_HEAD(self):
        """Handle HEAD requests, same routing logic as GET requests"""
        print(f"HEAD request: {self.path}")
        if self.path.startswith('/api/'):
            print("Handling API request")
            self.handle_api_request()
        elif self.path.startswith('/videos/'):
            print("Handling video HEAD request")
            self.handle_video_head_request()
        elif self.path.startswith('/images/'):
            print("Handling image HEAD request")
            self.handle_image_head_request()
        else:
            print("Handling static file HEAD request")
            # Handle static files
            super().do_HEAD()

    def handle_api_request(self):
        """Handle API requests, proxy to backend"""
        try:
            # Build backend URL
            backend_url = f"http://localhost:8081{self.path[4:]}"  # Remove /api prefix
            
            # Get request body
            content_length = int(self.headers.get('Content-Length', 0))
            request_body = self.rfile.read(content_length) if content_length > 0 else b''
            
            # Create proxy request
            req = urllib.request.Request(backend_url, data=request_body, method=self.command)
            
            # Copy relevant request headers
            for header_name, header_value in self.headers.items():
                if header_name.lower() not in ['host', 'connection']:
                    req.add_header(header_name, header_value)
            
            # Make the request
            with urllib.request.urlopen(req) as response:
                # Send response status
                self.send_response(response.status)
                
                # Copy response headers
                for header_name, header_value in response.headers.items():
                    if header_name.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header_name, header_value)
                self.end_headers()
                
                # Copy response body
                if self.command != 'HEAD':
                    self.wfile.write(response.read())
            
        except HTTPError as e:
            self.send_error(e.code, e.reason)
        except Exception as e:
            print(f"Error handling API request: {e}")
            self.send_error(500, "Internal Server Error")

    def handle_image_request(self):
        """Handle image file requests"""
        try:
            # Extract filename from path
            filename = self.path[8:]  # Remove /images/ prefix
            
            # 首先尝试直接在images目录中查找
            image_path = os.path.join("uploads", "images", filename)
            
            print(f"Looking for image file: {image_path}")
            
            if os.path.exists(image_path):
                print(f"Image file found: {image_path}")
                self.send_response(200)
                
                # Determine content type based on file extension
                if filename.lower().endswith('.png'):
                    content_type = 'image/png'
                elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif filename.lower().endswith('.gif'):
                    content_type = 'image/gif'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(os.path.getsize(image_path)))
                self.end_headers()
                
                with open(image_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            
            # 如果直接路径不存在，在images目录的子目录中搜索
            images_dir = os.path.join("uploads", "images")
            if os.path.exists(images_dir):
                print(f"Searching in subdirectories of {images_dir}")
                for root, dirs, files in os.walk(images_dir):
                    if filename in files:
                        found_path = os.path.join(root, filename)
                        print(f"Found image file in subdirectory: {found_path}")
                        
                        self.send_response(200)
                        
                        # Determine content type based on file extension
                        if filename.lower().endswith('.png'):
                            content_type = 'image/png'
                        elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                            content_type = 'image/jpeg'
                        elif filename.lower().endswith('.gif'):
                            content_type = 'image/gif'
                        else:
                            content_type = 'application/octet-stream'
                        
                        self.send_header('Content-Type', content_type)
                        self.send_header('Content-Length', str(os.path.getsize(found_path)))
                        self.end_headers()
                        
                        with open(found_path, 'rb') as f:
                            self.wfile.write(f.read())
                        return
            
            print(f"Image file not found: {image_path}")
            self.send_error(404, "Image not found")
                
        except Exception as e:
            print(f"Error handling image request: {e}")
            self.send_error(500, "Internal Server Error")

    def handle_video_request(self):
        """Handle video file requests"""
        try:
            # Extract filename from path
            filename = self.path[8:]  # Remove /videos/ prefix
            
            # 首先尝试直接在videos目录中查找
            video_path = os.path.join("uploads", "videos", filename)
            
            print(f"Looking for video file: {video_path}")
            
            if os.path.exists(video_path):
                print(f"Video file found: {video_path}")
                self.send_response(200)
                self.send_header('Content-Type', 'video/mp4')
                self.send_header('Content-Length', str(os.path.getsize(video_path)))
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()
                
                with open(video_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            
            # 如果直接路径不存在，在videos目录的子目录中搜索
            videos_dir = os.path.join("uploads", "videos")
            if os.path.exists(videos_dir):
                print(f"Searching in subdirectories of {videos_dir}")
                for root, dirs, files in os.walk(videos_dir):
                    if filename in files:
                        found_path = os.path.join(root, filename)
                        print(f"Found video file in subdirectory: {found_path}")
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'video/mp4')
                        self.send_header('Content-Length', str(os.path.getsize(found_path)))
                        self.send_header('Accept-Ranges', 'bytes')
                        self.end_headers()
                        
                        with open(found_path, 'rb') as f:
                            self.wfile.write(f.read())
                        return
            
            print(f"Video file not found: {video_path}")
            self.send_error(404, "Video not found")
                
        except Exception as e:
            print(f"Error handling video request: {e}")
            self.send_error(500, "Internal Server Error")

    def handle_image_head_request(self):
        """Handle HEAD requests for image files"""
        try:
            filename = self.path[8:]  # Remove /images/ prefix
            
            # 首先尝试直接在images目录中查找
            image_path = os.path.join("uploads", "images", filename)
            
            if os.path.exists(image_path):
                self.send_response(200)
                
                # Determine content type based on file extension
                if filename.lower().endswith('.png'):
                    content_type = 'image/png'
                elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif filename.lower().endswith('.gif'):
                    content_type = 'image/gif'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(os.path.getsize(image_path)))
                self.end_headers()
                return
            
            # 如果直接路径不存在，在images目录的子目录中搜索
            images_dir = os.path.join("uploads", "images")
            if os.path.exists(images_dir):
                for root, dirs, files in os.walk(images_dir):
                    if filename in files:
                        found_path = os.path.join(root, filename)
                        
                        self.send_response(200)
                        
                        # Determine content type based on file extension
                        if filename.lower().endswith('.png'):
                            content_type = 'image/png'
                        elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                            content_type = 'image/jpeg'
                        elif filename.lower().endswith('.gif'):
                            content_type = 'image/gif'
                        else:
                            content_type = 'application/octet-stream'
                        
                        self.send_header('Content-Type', content_type)
                        self.send_header('Content-Length', str(os.path.getsize(found_path)))
                        self.end_headers()
                        return
            
            self.send_error(404, "Image not found")
                
        except Exception as e:
            print(f"Error handling image HEAD request: {e}")
            self.send_error(500, "Internal Server Error")

    def handle_video_head_request(self):
        """Handle HEAD requests for video files"""
        try:
            filename = self.path[8:]  # Remove /videos/ prefix
            
            # 首先尝试直接在videos目录中查找
            video_path = os.path.join("uploads", "videos", filename)
            
            if os.path.exists(video_path):
                self.send_response(200)
                self.send_header('Content-Type', 'video/mp4')
                self.send_header('Content-Length', str(os.path.getsize(video_path)))
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()
                return
            
            # 如果直接路径不存在，在videos目录的子目录中搜索
            videos_dir = os.path.join("uploads", "videos")
            if os.path.exists(videos_dir):
                for root, dirs, files in os.walk(videos_dir):
                    if filename in files:
                        found_path = os.path.join(root, filename)
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'video/mp4')
                        self.send_header('Content-Length', str(os.path.getsize(found_path)))
                        self.send_header('Accept-Ranges', 'bytes')
                        self.end_headers()
                        return
            
            self.send_error(404, "Video not found")
                
        except Exception as e:
            print(f"Error handling video HEAD request: {e}")
            self.send_error(500, "Internal Server Error")

    def do_OPTIONS(self):
        """Handle OPTIONS requests (CORS preflight)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def main():
    port = 8080
    print(f"Starting proxy server on port {port}")
    print("Frontend files served from: vue-login-demo-master/dist")
    print("API requests proxied to: http://localhost:8081")
    print("Video files served from: uploads/videos/")
    print("Image files served from: uploads/images/")
    
    with socketserver.TCPServer(("", port), ProxyHandler) as httpd:
        print(f"Proxy server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down proxy server...")
            httpd.shutdown()

if __name__ == "__main__":
    main() 