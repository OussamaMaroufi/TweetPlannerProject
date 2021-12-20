import { createContext, useState, useEffect } from 'react'
import { Navigate } from 'react-router-dom'

const FeedbackContext = createContext()



export const FeedbackProvider = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true)
  const [feedback, setFeedback] = useState([])
  const [token,setToken] = useState(null)
  const [previousLink, setPreviousLink] = useState(null)
  const [nextLink,setNextLink] = useState(null)
  const [feedbackEdit, setFeedbackEdit] = useState({
    item: {},
    edit: false,
  })

  const filters = [{id:-1 ,label:"All"},{id:0 ,label:"Football"},{id:1 ,label:"Men's Basketball"},{id:2 ,label:"Women's basketball"},
  {id:3 ,label:"Softball"},{id:4 ,label:"Baseball"},{id:5 ,label:"Campus"}]


  useEffect(() => {
    fetchFeedback()
    let token=localStorage.getItem('token')
    setToken(token)
  }, [])

  // Fetch feedback
  const fetchFeedback = async (page=1,categoryFilter=null,statusFilter=null,paginationURL=null) => {
    let url;
    if(paginationURL) {url = paginationURL}
    else{
      url = `http://127.0.0.1:8000/posts/?page=${page}`
    //console.log(category,status);
    if(categoryFilter)
      url = `${url}&topic=${categoryFilter}`
    if(statusFilter !== null)
      url = `${url}&isPublished=${statusFilter}`
    }
    console.log(url)
    
    const response = await fetch(url,{"headers":{"Content-type": "application/json; charset=UTF-8"}})
    const data = await response.json()
    console.log(data)
    setFeedback(data['results'])
    setIsLoading(false)
    setNextLink(data['links']['next'])
    setPreviousLink(data['links']['previous'])
      

  }

  // Add feedback
  const addFeedback = async (newFeedback) => {
    var formdata = new FormData();
    formdata.append("content", newFeedback.text);
    if (newFeedback.media)
      formdata.append("postImage", newFeedback.media, newFeedback.media['name']);
    formdata.append("topic", newFeedback.category );
    formdata.append("postTime", newFeedback.postTime+":00Z");
    
    var requestOptions = {
      method: 'POST',
      body: formdata,
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:8000/post/create/", requestOptions)
      .then(response => response.text())
      .then(result => {
        alert("The post has been added successfully!")
        console.log(result);
        result = JSON.parse(result)
        setFeedback([{
        content: result.content,
        isPublished: result.isPublished,
        postImage: result.postImage,
        postTime: result.postTime,
        topic: result.topic,

      },...feedback])})
      .catch(error => console.log('error', error));
      
      
  }

  // Delete feedback
  const deleteFeedback = async (id) => {
    if (window.confirm('Are you sure you want to delete?')) {
      await fetch(`http://127.0.0.1:8000/post/delete/${id}`, { method: 'DELETE' })

      setFeedback(feedback.filter((item) => item.id !== id))
    }
  }

  // Update feedback item
  const updateFeedback = async (id, updItem) => {
    var formdata = new FormData();
    formdata.append("content", updItem.text);
    if (updItem.media)
      formdata.append("postImage", updItem.media, updItem.media['name']);
    formdata.append("topic", updItem.category );
    formdata.append("postTime", updItem.postTime+":00Z");
    
    var requestOptions = {
      method: 'PUT',
      body: formdata,
      redirect: 'follow'
    };
    
    fetch(`http://127.0.0.1:8000/post/update/${id}/`, requestOptions)
      .then(response => response.text())
      .then(result => {
        console.log(result)
        result = JSON.parse(result)
        setFeedback(feedback.map(feed=>id==feed.id ? 
          {
            id,
            content: result.content,
            isPublished: result.isPublished,
            postImage: result.postImage,
            postTime: result.postTime,
            topic: result.topic,
          }
          : feed))
      })
      .catch(error => console.log('error', error));
      
      
  }

  // Set item to be updated
  const editFeedback = (item) => {
    setFeedbackEdit({
      item,
      edit: true,
    })
  }

const login = (username,password)=>{

  var formdata = new FormData();
formdata.append("username", username);
formdata.append("password", password);

var requestOptions = {
  method: 'POST',
  body: formdata,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/login/", requestOptions)
  .then(response => response.text())
  .then(result => {
    console.log(result)
    result = JSON.parse(result)
    setToken(result['token'])
    localStorage.setItem('token',result['token'])
    
  })
  .catch(error => console.log('error', error));
  
}

const logout = (e)=>{
  localStorage.removeItem('token')
  setToken(null)
};


const isLoggedIn = ()=>{
  let token = localStorage.getItem('token')
  return token ? true: false
}

  return (
    <FeedbackContext.Provider
      value={{
        feedback,
        feedbackEdit,
        isLoading,
        filters,
        token,
        nextLink,
        previousLink,
        deleteFeedback,
        addFeedback,
        editFeedback,
        updateFeedback,
        fetchFeedback,
        login,
        isLoggedIn,
        logout,
      }}
    >
      {children}
    </FeedbackContext.Provider>
  )
}

export default FeedbackContext
