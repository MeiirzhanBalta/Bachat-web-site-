javascript
Копировать код
<template>
  <div class="upload-container">
    <h1>Uploading and downloading documents</h1>
    <label for="file-upload" class="file-label">Select file</label>
    <input id="file-upload" type="file" @change="handleFileUpload" class="file-input" />
    <button @click="submitFile" class="upload-button">Upload file</button>
    <div v-if="documents.length > 0" class="document-list">
      <h1>List of documents:</h1>
      <ul class="no-bullets">
        <li v-for="doc in documents" :key="doc.id" class="document-item">
          <span class="document-name">{{ doc.file_name }}</span> - <span class="document-date">{{ doc.created_at }}</span>
          <button @click="downloadFile(doc.id)" class="download-button">Download</button>
          <button @click="deleteFile(doc.id)" class="delete-button">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      documents: []
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      axios.post('http://bachattv.com:5000/api/upload-document', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
      })
      .then(response => {
        console.log('File uploaded successfully:', response.data);
        this.fetchDocuments();
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
    },
    fetchDocuments() {
      axios.get('http://bachattv.com:5000/documents', { withCredentials: true })
        .then(response => {
          this.documents = response.data;
        })
        .catch(error => {
          console.error('Error fetching list of documents:', error);
        });
    },
    downloadFile(documentId) {
      window.open(`http://bachattv.com:5000/download/${documentId}`, '_blank');
    },
    deleteFile(documentId) {
      axios.delete(`http://bachattv.com:5000/documents/${documentId}`, { withCredentials: true })
        .then(response => {
          console.log('File deleted successfully:', response.data);
          this.fetchDocuments();
        })
        .catch(error => {
          console.error('Error deleting file:', error);
        });
    }
  },
  created() {
    this.fetchDocuments();
  }
};
</script>

<style scoped>
.upload-container {
  background-color: #f0f0f0;
}
.upload-container {
  max-width: 1150px;
  margin: 0 auto;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 5px 5px rgba(0, 0, 0, 0.10);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.file-label {
  display: block;
  margin-bottom: 10px;
}

.file-input {
  display: block;
  padding: 10px;
  margin-bottom: 20px;
}

.upload-button {
  display: block;
  margin-bottom: 20px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

.document-list {
  margin-top: 30px;
}

.document-item {
  margin-bottom: 20px;
}

.document-name {
  font-weight: bold;
}

.download-button {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  background-color: #28a745;
  color: #fff;
  cursor: pointer;
}

.delete-button {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  background-color: #dc3545;
  color: #fff;
  cursor: pointer;
  margin-left: 10px;
}

.document-date {
  color: #777;
}

.no-bullets {
  list-style-type: none;
  padding-left: 0;
}
</style>
