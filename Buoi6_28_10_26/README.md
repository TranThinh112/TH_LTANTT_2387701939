# BÁO CÁO THỰC HÀNH BUỔI 6: BẢO MẬT VỚI DEVSECOPS & CI/CD PIPELINE TRÊN GITLAB

- **Học phần:** Thực hành Lập trình An toàn Thông tin
- **Mã số sinh viên (MSSV):** 2387701939
- **Họ và tên:** Trường Thịnh
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

### Bước 2: Mở dự án trong VS Code & cài đặt gói phụ thuộc
- Mở thư mục `pipeline-tutorial` bằng Visual Studio Code, kiểm tra cấu trúc thư mục và chạy lệnh cài đặt package nếu cần (`npm install`).

![Mở dự án trong Visual Studio Code](image/Screenshot%202026-10-28%20093710.png)

### Bước 3: Chạy thử nghiệm môi trường phát triển cục bộ (Local Server)
- Thực thi lệnh:
  ```bash
  npm start
  ```
- Docusaurus server khởi chạy thành công tại `http://localhost:3000`. Giao diện web hiển thị chính xác trên trình duyệt máy tính.

![Kiểm tra Docusaurus chạy tại localhost:3000](image/Screenshot%202026-10-28%20093934.png)

### Bước 4: Kiểm tra quá trình Build tĩnh (Production Build)
- Chạy thử lệnh build tĩnh để kiểm tra tính toàn vẹn của mã nguồn:
  ```bash
  npm run build
  ```
- Docusaurus biên dịch mã nguồn thành công và tạo thư mục chứa website tĩnh tại thư mục `build/`.

![Build tĩnh thành công bằng npm run build](image/Screenshot%202026-10-28%20094039.png)

### Bước 5: Cấu hình tệp .gitlab-ci.yml cho Docusaurus & GitLab Pages
- Tạo tệp `.gitlab-ci.yml` trong thư mục gốc của dự án `pipeline-tutorial` với image Docker `node:18` (hoặc `node:lts`), cấu hình cache `node_modules` và artifact đầu ra thư mục `public/`:

```yaml
image: node:18

pages:
  stage: deploy
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
  before_script:
    - npm ci --cache .npm --prefer-offline
  script:
    - npm run build
    - mv build public
  artifacts:
    paths:
      - public
  only:
    - main
```

![Tạo cấu hình CI/CD cho Docusaurus Pages](image/Screenshot%202026-10-28%20094254.png)

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
- Nhấp vào job `pages` để theo dõi tiến trình thực tế: các bước tải image node, restore cache, chạy lệnh `npm run build`, di chuyển `build` sang `public` và upload artifacts đều kết thúc với mã thoát `Job succeeded`.

![Log chi tiết của job pages thành công](image/Screenshot%202026-10-28%20094654.png)

### Bước 9: Thiết lập và kiểm tra đường dẫn GitLab Pages
- Truy cập vào **Deploy** -> **Pages** trong repository GitLab để lấy đường dẫn website được xuất bản: `https://truongthinh-2387701939-fa3ba8.gitlab.io/`.
- **Lưu ý cấu hình URL & BaseUrl trong `docusaurus.config.js`:**
  - Nếu dự án nằm ở root domain của GitLab Pages, cấu hình:
    ```js
    url: 'https://truongthinh-2387701939-fa3ba8.gitlab.io',
    baseUrl: '/',
    ```
  - Cấu hình chuẩn xác giúp tránh lỗi vỡ giao diện (404 CSS/JS/Assets).

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
| 9 | `Screenshot 2026-10-28 093710.png` | Cài đặt và mở dự án Docusaurus trong VS Code | Hoàn thành |
| 10 | `Screenshot 2026-10-28 093934.png` | Khởi chạy server local `npm start` trên port 3000 | Hoàn thành |
| 11 | `Screenshot 2026-10-28 094039.png` | Kiểm tra lệnh `npm run build` tạo thư mục static | Hoàn thành |
| 12 | `Screenshot 2026-10-28 094254.png` | Viết cấu hình `.gitlab-ci.yml` triển khai Pages | Hoàn thành |
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
