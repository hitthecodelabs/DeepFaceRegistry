import axios from 'axios';

axios.interceptors.request.use((req) => {
    if (!req.url.includes('login') || !req.url.includes('logout')) {
      const token = localStorage.getItem('token')
      req.headers = {
        Authorization: `Token ${token}`,
      }
    }
    return req
});

export default axios;