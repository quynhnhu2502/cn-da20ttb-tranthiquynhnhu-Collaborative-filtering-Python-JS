//Sử dụng ngôn ngữ lập trình JavaScript và thư viện React để xây dựng giao diện người dùng.

import axios from 'axios'; // Import Axios để thực hiện yêu cầu HTTP
import './App.css'; // import một tệp CSS để tùy chỉnh giao diện
import GridLoader from "react-spinners/GridLoader"; // import GridLoader từ thư viện react-spinners để hiển thị hiệu ứng loading
import { useState, useEffect } from 'react'; // import useState và useEffect để quản lý state và thực hiện các tác vụ sau mỗi lần render.

function App() {
  const [list, setList] = useState([]);
  const [isSearch, setIsSearch] = useState(false);
  const [text,setText] = useState("");

  const search = async(name) =>{
    try {
      const response = await axios.get(`http://127.0.0.1:5000/recommend/${name}`);
      if(response.data){
        setIsSearch(false);
        setList(response?.data?.recommendations);
      }
    } catch (error) {
      setIsSearch(false);
      console.log(error);
    }
  }

  const handleSearch = async() =>{
    if(!text) return;
    setIsSearch(true);
    await search(text);
  }

  return (
    <>
      <div className='search-container'>
          <div className="header">
            <input type="text" value={text} onChange={(e)=>setText(e.target.value)} className="input-search" placeholder='Vui lòng nhập tên phim...'/>
            {
              text && (
                <button className="search-btn" onClick={handleSearch}>
              Tìm kiếm
            </button>
              )
            }
          </div>
          {
            !isSearch && list.length > 0 && (
              <div className="form">
            <h1 className="title">Ket qua ({list.length})</h1>
            <div className="list-item">
              {
                list?.map((item, index)=>(
                  <div className="item" key={index}>
                <h1>{item?.Name}</h1>
                <p>{item?.count} count</p>
              </div>
                ))
              }
            </div>
          </div>
            )
          }
          {
            isSearch && (
              <div className="form-loading">
            <GridLoader color="#FFCCCC" size={20}/>
            </div>
            )
          }
      </div>
    </>
  );
}

export default App;
