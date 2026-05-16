import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_HOST_IP || `http://${window.location.hostname}:8080`;

function makeClient(baseURL) {
  const client = axios.create({ baseURL })
  client.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })
  return client
}

export const paymentClient = makeClient(BACKEND_URL+'/payments')

export async function createPayment(order_id, amount, currency = 'KZT', method = 'card') {
  const { data } = await paymentClient.post('/payments', { 
    order_id, 
    amount, 
    currency, 
    method 
  })
  return data
}

export async function getPayment(payment_id) {
  const { data } = await paymentClient.get(`/payments/${payment_id}`)
  return data
}

export async function getAllPayments() {
  const { data } = await paymentClient.get('/payments')
  return data
}

export async function processPayment(payment_id) {
  const { data } = await paymentClient.post(`/payments/${payment_id}/process`)
  return data
}

export async function refundPayment(payment_id) {
  const { data } = await paymentClient.post(`/payments/${payment_id}/refund`)
  return data
}
