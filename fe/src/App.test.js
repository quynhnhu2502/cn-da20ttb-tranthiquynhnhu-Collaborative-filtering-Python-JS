// kiểm thử (unit test) sử dụng thư viện @testing-library/react để kiểm tra rằng một thành phần cụ thể 
// trong ứng dụng React (App component) được hiển thị đúng cách

import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
