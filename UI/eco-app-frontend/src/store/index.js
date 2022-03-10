import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    temperature_data: {},
    location: {},
    modalInfo:{
      isVisible:false,
      ModalTitle:"",
      ModalInfo:""
    },
    loader: false,
    dateSelected:""
  },
  getters: {
  },
  mutations: {
    SET_TEMPERATURE_DATA: (state, payload)=>{
      state.temperature_data = payload
    },
    SET_LOCATION: (state, payload) =>{
      state.location = payload
    },
    SET_MODAL_DATA: (state, payload)=>{
      state.modalInfo = {...state.modalInfo, ...payload,}
    },
    TOGGLE_LOADER: (state, payload)=>{
        state.loader = payload
    },
    SET_DATE_SELECTED: (state, payload)=>{
      state.dateSelected = payload
    }
  },
  actions: {
    set_location: (context, location) => {
      context.commit('SET_LOCATION', location)
    },
    async get_temperature_data(context, location){
      let host = "localhost" // process.env.VUE_APP_API_HOST
      let port = "8081" //process.env.VUE_APP_API_PORT
      await axios.get(`http://${host}:${port}/temperature/${location.toString()}`)
          .then(response => {
            context.commit('SET_TEMPERATURE_DATA', response.data)
          })
          .catch(error => {
            let errorMessage = "Failed to serve the request"
            if (error.response) {
              errorMessage = error.response.data
            } else if (error.request) {
              errorMessage = error.request
            } else {
              errorMessage =  error.message
            }
            context.commit("TOGGLE_LOADER", false)
            context.commit("SET_MODAL_DATA",
                { isVisible:true,
                  ModalTitle:"Dang! It didn't go through!",
                  ModalInfo:errorMessage
                })
          })
    },
    set_modal_visibility: (context, payload)=>{
      context.commit("SET_MODAL_VISIBILITY", payload)
    }

  },
  modules: {
  }
})
