import { AuthApiAdapter } from '../infrastructure/api/AuthApiAdapter.js';
import { CuartoApiAdapter } from '../infrastructure/api/CuartoApiAdapter.js';
import { ReservaApiAdapter } from '../infrastructure/api/ReservaApiAdapter.js';

const BACKEND_URL = 'http://localhost:8000';
export const authAdapter = new AuthApiAdapter(BACKEND_URL);
export const cuartoAdapter = new CuartoApiAdapter(BACKEND_URL);
export const reservaAdapter = new ReservaApiAdapter(BACKEND_URL);