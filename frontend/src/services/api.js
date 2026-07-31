import axios from 'axios';

const API_BASE_URL = '/api';

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const getModelInfo = async () => {
  const response = await axios.get(`${API_BASE_URL}/model-info`);
  return response.data;
};

export const checkHealth = async () => {
  const response = await axios.get(`${API_BASE_URL}/health`);
  return response.data;
};
