import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://172.234.123.78:5000',
  withCredentials: true,  
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

const ApiService = {
  init() {},
  post(endpoint, body) {
    return apiClient.post(endpoint, body);
  },
  get(endpoint) {
    return apiClient.get(endpoint);
  },
  login(credentials) {
    return apiClient.post('/login', credentials);
  },
  loadUserInfo() {
    return apiClient.get('/user-info');
  },
  sendMessageToBot(message) {
    return apiClient.post('/api/send-message', { message });
  },
  getChatHistory() {
    return apiClient.get('/api/chat-history');
  },
  uploadDocument(file) {
    let formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/api/upload-document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  fetchDocuments() {
    return apiClient.get('/documents');
  },
  downloadDocument(documentId) {
    return apiClient.get(`/download/${documentId}`, {
      responseType: 'blob'
    });
  },
  deleteDocument(documentId) {
    return apiClient.delete(`/documents/${documentId}`);
  },
  addSale(sale) {
    return apiClient.post('/sales', sale);
  },
  fetchSales() {
    return apiClient.get('/sales');
  },
  deleteSale(saleId) {
    return apiClient.delete(`/sales/${saleId}`);
  }
};

export default ApiService;

