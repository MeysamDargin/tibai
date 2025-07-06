import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';
export const feedbackService = {
    postfeedback: (name, lastName, email, feedback) => apiClient.post(ENDPOINTS.FEEDBACK, { name, lastName, email, feedback }),
};