# BÁO CÁO THỰC HÀNH BUỔI 6: BẢO MẬT VỚI DEVSECOPS & CI/CD PIPELINE TRÊN GITLAB

- **Học phần:** Thực hành Lập trình An toàn Thông tin
- **Mã số sinh viên (MSSV):** 2387701939
- **Họ và tên:** Trương Thịnh
- **GitLab Username:** `ttthinh2005`
- **GitLab Repository:** `truongthinh-2387701939`
- **Trang GitLab Pages trực tiếp:** [https://truongthinh-2387701939-fa3ba8.gitlab.io/](https://truongthinh-2387701939-fa3ba8.gitlab.io/)

---

## I. MỤC TIÊU VÀ TỔNG QUAN LÝ THUYẾT

### 1. Mục tiêu bài lab
1. Hiểu được khái niệm **DevSecOps** và vai trò của việc tích hợp bảo mật vào quy trình phát triển/triển khai liên tục (CI/CD).
2. Nắm vững cấu trúc và cú pháp của tệp cấu hình `.gitlab-ci.yml` trên GitLab.
3. Tạo và quản lý CI/CD Pipeline với các giai đoạn chuẩn: `build`, `test`, `deploy`.
4. Khởi tạo một dự án web tĩnh bằng **Docusaurus**, cấu hình và tự động hóa quy trình triển khai lên **GitLab Pages** thông qua GitLab CI Runner.
5. Xử lý các lỗi cấu hình phổ biến khi build/deploy (đường dẫn `baseUrl`, artifact `public/`).

### 2. Tổng quan kiến thức DevSecOps
- **DevSecOps** là phương pháp tích hợp triệt để yếu tố an toàn thông tin (Security) vào mọi giai đoạn của vòng đời phát triển phần mềm (SDLC), thay vì chỉ kiểm tra ở khâu cuối cùng ("Shift-Left Security").
- **CI (Continuous Integration):** Tự động hóa tích hợp code từ nhiều lập trình viên, tự động build và chạy test nhằm phát hiện lỗi sớm.
- **CD (Continuous Deployment / Delivery):** Tự động đóng gói và triển khai sản phẩm lên môi trường staging hoặc production khi các bài kiểm tra đã vượt qua.
- **Các thành phần bảo mật trong DevSecOps Pipeline:**
  - **SAST (Static Application Security Testing):** Phân tích mã nguồn tĩnh để tìm lỗ hổng bảo mật tiềm ẩn.
  - **SCA (Software Composition Analysis):** Quét các thư viện phụ thuộc (dependencies) để tìm CVE đã biết.
  - **Secret Detection:** Ngăn chặn việc vô tình commit các thông tin nhạy cảm (API Keys, Passwords, Tokens).
  - **DAST (Dynamic Application Security Testing):** Kiểm thử động ứng dụng đang chạy để phát hiện lỗ hổng thời gian thực.

---

## II. BÀI 1: KHỞI TẠO DỰ ÁN VÀ XÂY DỰNG GITLAB CI/CD PIPELINE CƠ BẢN

### Bước 1: Tạo dự án mới trên GitLab
- Đăng nhập vào GitLab với tài khoản `ttthinh2005`.
- Chọn **New project** -> **Create blank project**.
- Đặt tên Project Name: `truongthinh-2387701939`, chế độ hiển thị: Public.

![Tạo mới Project trên GitLab](image/Screenshot%202026-10-28%20084615.png)

### Bước 2: Khởi tạo Repository trên GitLab
- Dự án được tạo thành công với cấu trúc kho lưu trữ rỗng, sẵn sàng để cấu hình CI/CD và đẩy mã nguồn.

![Khởi tạo repository thành công](image/Screenshot%202026-10-28%20084842.png)

### Bước 3: Điều hướng tới mục CI/CD Pipelines
- Trong thanh menu điều hướng bên trái của GitLab, truy cập vào **Build** -> **Pipeline editor** hoặc **Pipelines** để bắt đầu thiết lập pipeline tự động.

![Truy cập mục CI/CD Pipelines](image/Screenshot%202026-10-28%20084947.png)

### Bước 4: Mở giao diện GitLab Pipeline Editor
- Nhấn chọn **Configure pipeline** để mở trình biên tập trực quan `.gitlab-ci.yml`.

![Mở giao diện Pipeline Editor](image/Screenshot%202026-10-28%20085029.png)

### Bước 5: Viết cấu hình Pipeline cơ bản (.gitlab-ci.yml)
- Thiết lập tệp `.gitlab-ci.yml` định nghĩa các giai đoạn (`build`, `test`, `deploy`) cùng các lệnh script thực thi tương ứng:

```yaml
stages:
  - build
  - test
  - deploy

build-job:
  stage: build
  script:
    - echo "Compiling the code..."
    - echo "Compile complete."

test-job:
  stage: test
  script:
    - echo "Running unit tests..."
    - echo "Code coverage 90%."

deploy-job:
  stage: deploy
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed."
```

![Viết cấu hình .gitlab-ci.yml](image/Screenshot%202026-10-28%20085102.png)

### Bước 6: Commit tệp cấu hình lên nhánh main
- Nhập commit message mô tả hành động (ví dụ: `ci: add gitlab-ci.yml`) và nhấn **Commit changes** để lưu lại cấu hình và kích hoạt pipeline lần đầu.

![Commit tệp .gitlab-ci.yml](image/Screenshot%202026-10-28%20085212.png)

### Bước 7: Kiểm tra kết quả thực thi Pipeline cơ bản
- Pipeline chạy tự động trên GitLab Shared Runner. Cả 3 job (`build-job`, `test-job`, `deploy-job`) đều hoàn thành ở trạng thái **Passed** màu xanh lá.

![Pipeline cơ bản chạy thành công 3 stages](image/Screenshot%202026-10-28%20085456.png)

---

## III. BÀI 2: TRIỂN KHAI TRANG DOCUSAURUS TỰ ĐỘNG LÊN GITLAB PAGES BẰNG CI/CD

### Bước 1: Khởi tạo ứng dụng Docusaurus trên máy cục bộ
- Sử dụng lệnh `npx create-docusaurus@latest pipeline-tutorial classic` trên terminal máy tính để tạo dự án Docusaurus template classic.

![Khởi tạo dự án Docusaurus cục bộ](image/Screenshot%202026-10-28%20093425.png)

### Bước 2: Chạy thử nghiệm môi trường phát triển cục bộ (Local Server)
- Mở thư mục `pipeline-tutorial` trong Visual Studio Code, khởi chạy server phát triển cục bộ bằng lệnh:
  ```bash
  npm start
  ```
- Docusaurus server biên dịch và khởi chạy thành công tại cổng local: `http://localhost:3000/`.

![Khởi chạy server Docusaurus local tại localhost:3000](image/Screenshot%202026-10-28%20093710.png)

### Bước 3: Kiểm tra và chỉnh sửa cấu hình `docusaurus.config.js`
- Mở file `docusaurus.config.js` để cấu hình thông số tên trang, `url` và `baseUrl` phục vụ việc deploy lên GitLab Pages.
- Cấu hình địa chỉ url trỏ về trang GitLab Pages:
  ```javascript
  url: 'https://truongthinh-2387701939-fa3ba8.gitlab.io',
  baseUrl: '/',
  ```

![Cấu hình file docusaurus.config.js](image/Screenshot%202026-10-28%20093934.png)

### Bước 4: Tạo tệp cấu hình `.gitlab-ci.yml` cho dự án Docusaurus
- Tạo file `.gitlab-ci.yml` trong thư mục gốc của project để định nghĩa 2 stage: `build` (dùng container `node:latest`, chạy `npm install` và `npm run build`) và `pages` (di chuyển thư mục `build/` thành `public/` để GitLab Pages nhận diện):

```yaml
stages:
  - build
  - deploy

build-job:
  stage: build
  image: node:latest
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - "build/"

pages:
  stage: deploy
  script:
    - mv build/ public/
  artifacts:
    paths:
      - "public/"
```

![Tạo cấu hình .gitlab-ci.yml cho Docusaurus](image/Screenshot%202026-10-28%20094039.png)

### Bước 5: Chạy thử lệnh `npm run build` kiểm tra đóng gói cục bộ
- Thực hiện chạy lệnh build trên terminal:
  ```bash
  npm run build
  ```
- Docusaurus đóng gói thành công mã nguồn tĩnh vào thư mục `build/` mà không phát sinh lỗi cú pháp hay thiếu plugin.

![Kiểm tra build tĩnh bằng npm run build thành công](image/Screenshot%202026-10-28%20094254.png)

### Bước 6: Đẩy mã nguồn từ máy tính lên GitLab Repository
- Liên kết remote repository GitLab và đẩy toàn bộ source code lên nhánh `main`:
  ```bash
  git add .
  git commit -m "feat: init docusaurus and gitlab pages pipeline"
  git push -u origin main
  ```

![Git add, commit và push lên GitLab](image/Screenshot%202026-10-28%20094412.png)

### Bước 7: Kích hoạt Pipeline tự động trên GitLab
- Sau khi push code, GitLab CI/CD tự động trigger pipeline mới để thực hiện tiến trình đóng gói và build trang Docusaurus.

![Pipeline tự động được kích hoạt trên GitLab](image/Screenshot%202026-10-28%20094610.png)

### Bước 8: Kiểm tra chi tiết log thực thi của Job `pages`
- Nhấp vào job `pages` để theo dõi tiến trình thực tế: các bước tải container, chạy lệnh build, di chuyển thư mục `build/` sang `public/` và upload artifacts đều hoàn thành thành công (`Job succeeded`).

![Log chi tiết của job pages thành công](image/Screenshot%202026-10-28%20094654.png)

### Bước 9: Thiết lập và kiểm tra đường dẫn GitLab Pages
- Truy cập vào **Deploy** -> **Pages** trong repository GitLab để lấy đường dẫn website được xuất bản: `https://truongthinh-2387701939-fa3ba8.gitlab.io/`.

![Kiểm tra cấu hình Pages URL trên GitLab](image/Screenshot%202026-10-28%20094751.png)

### Bước 10: Nghiệm thu trang Docusaurus hoàn chỉnh trên Internet
- Truy cập vào đường dẫn Pages trực tiếp [https://truongthinh-2387701939-fa3ba8.gitlab.io/](https://truongthinh-2387701939-fa3ba8.gitlab.io/).
- Trang web tải nhanh, đầy đủ CSS, logo, các trang tài liệu (Tutorial Docs, Blog) và các nút tương tác hoạt động hoàn hảo.

![Website Docusaurus hoạt động hoàn chỉnh trên GitLab Pages](image/Screenshot%202026-10-28%20095340.png)

---

## IV. BẢNG TỔNG HỢP CÁC HÌNH ẢNH MINH CHỨNG (17 ẢNH)

| STT | Tên file ảnh | Mô tả bước thực hiện | Trạng thái |
|:---:|:---|:---|:---:|
| 1 | `Screenshot 2026-10-28 084615.png` | Tạo project mới `truongthinh-2387701939` trên GitLab | Hoàn thành |
| 2 | `Screenshot 2026-10-28 084842.png` | Giao diện repository ban đầu sau khi tạo | Hoàn thành |
| 3 | `Screenshot 2026-10-28 084947.png` | Truy cập mục CI/CD Pipelines trong GitLab | Hoàn thành |
| 4 | `Screenshot 2026-10-28 085029.png` | Mở trình soạn thảo Pipeline Editor | Hoàn thành |
| 5 | `Screenshot 2026-10-28 085102.png` | Viết nội dung tệp `.gitlab-ci.yml` cơ bản | Hoàn thành |
| 6 | `Screenshot 2026-10-28 085212.png` | Commit tệp `.gitlab-ci.yml` lên branch main | Hoàn thành |
| 7 | `Screenshot 2026-10-28 085456.png` | Pipeline 3 stage (`build`, `test`, `deploy`) Passed | Hoàn thành |
| 8 | `Screenshot 2026-10-28 093425.png` | Khởi tạo dự án Docusaurus bằng `npx` | Hoàn thành |
| 9 | `Screenshot 2026-10-28 093710.png` | Chạy lệnh `npm start` khởi động server Docusaurus localhost:3000 | Hoàn thành |
| 10 | `Screenshot 2026-10-28 093934.png` | Cấu hình tham số `url` và `baseUrl` trong `docusaurus.config.js` | Hoàn thành |
| 11 | `Screenshot 2026-10-28 094039.png` | Viết cấu hình `.gitlab-ci.yml` (build và pages deploy) | Hoàn thành |
| 12 | `Screenshot 2026-10-28 094254.png` | Chạy thử nghiệm lệnh `npm run build` đóng gói static cục bộ | Hoàn thành |
| 13 | `Screenshot 2026-10-28 094412.png` | Commit và push toàn bộ source code lên GitLab | Hoàn thành |
| 14 | `Screenshot 2026-10-28 094610.png` | Pipeline Pages chạy tự động trên GitLab | Hoàn thành |
| 15 | `Screenshot 2026-10-28 094654.png` | Log thực thi chi tiết của job `pages` thành công | Hoàn thành |
| 16 | `Screenshot 2026-10-28 094751.png` | Cấu hình và đường dẫn GitLab Pages | Hoàn thành |
| 17 | `Screenshot 2026-10-28 095340.png` | Trang Docusaurus online hiển thị đầy đủ layout & css | Hoàn thành |

---

## V. KẾT LUẬN VÀ BÀI HỌC KINH NGHIỆM

1. **Hiệu quả của CI/CD:** Việc tự động hóa quá trình đóng gói và phát hành mã nguồn giúp giảm thiểu hoàn toàn sai sót thủ công, đồng thời rút ngắn thời gian đưa tính năng hoặc bản sửa lỗi tới người dùng cuối.
2. **Tích hợp DevSecOps:** Trong thực tế doanh nghiệp, pipeline cần bổ sung các công cụ bảo mật quét mã tự động (như GitLab SAST, SonarQube, Gitleaks, Trivy, Snyk) ngay trong pipeline trước khi cho phép tiến hành giai đoạn `deploy`.
3. **Quản lý Artifacts & Static Hosting:** Việc cấu hình đúng thư mục artifact đầu ra (GitLab Pages yêu cầu tên thư mục đích là `public/`) và cấu hình `baseUrl` chính xác là chìa khóa để triển khai thành công các ứng dụng web tĩnh nhiều trang.
