import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:2020',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  withCredentials: true, // برای ارسال و دریافت کوکی‌ها (مثل sessionid)
});

// ساده کردن interceptor (فقط لاگ و تنظیمات اولیه)
apiClient.interceptors.request.use((config) => {
  // چک کردن کوکی‌ها برای دیباگ
  const cookies = document.cookie.split('; ').reduce((acc, cookie) => {
    const [name, value] = cookie.split('=');
    acc[name] = value;
    return acc;
  }, {});
  console.log('Cookies being sent:', cookies);
  
  // اضافه کردن دستی sessionid به هدر از کوکی یا localStorage
  const sessionFromCookie = cookies.sessionid;
  const sessionFromStorage = localStorage.getItem('app_session');
  const sessionid = sessionFromCookie || sessionFromStorage;
  
  if (sessionid) {
    // ارسال توکن در هدر Authorization به صورت صریح
    config.headers['Authorization'] = `Session ${sessionid}`;
    // همچنین در کوکی هم ارسال می‌کنیم
    config.headers['Cookie'] = `sessionid=${sessionid}`;
  }

  // تنظیم Content-Type برای درخواست‌های فرم (مثل لاگین)
  if (config.formUrlEncoded) {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;