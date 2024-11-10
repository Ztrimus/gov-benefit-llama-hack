import api from './api';

export const getGrants = async () => {
  try {
    const response = await api.get('/grants');
    return response.data;
  } catch (error) {
    console.error("Error fetching grants", error);
    throw error;
  }
};

export const applyGrant = async (grantId) => {
  try {
    const response = await api.post('/apply-grant', { grant_id: grantId });
    return response.data;
  } catch (error) {
    console.error("Error applying for grant", error);
    throw error;
  }
};

export const getAppliedGrants = async () => {
  try {
    const response = await api.get('/applied-grants');
    return response.data;
  } catch (error) {
    console.error("Error fetching applied grants", error);
    throw error;
  }
};

export const updateGrantStatus = async (grantId, status, currentStatus) => {
  try {
    const response = await api.put('/update-grant-status', {
      grant_id: grantId,
      status: status,
      currentStatus: currentStatus,
    });
    return response.data;
  } catch (error) {
    console.error("Error updating grant status", error);
    throw error;
  }
};
