import LoginPage from "./login";
import Layout from '../app/layout'
import DashboardPage from "./dashboard"
import { Provider } from 'react-redux';
import store from '../redux/store';

export default function Main({ }) {
  return (
    <Provider store={store}>
      <Layout>
        <DashboardPage/>
      </Layout>
    </Provider>
  )
}