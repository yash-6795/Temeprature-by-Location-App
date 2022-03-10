<template>
  <v-app>
    <InfoModal></InfoModal>
    <LoadingModal></LoadingModal>
    <v-main>
    <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import InfoModal from "@/components/InfoModal";
import LoadingModal from "@/components/LoadingModal";

export default {
  name: 'App',
  components:{
    InfoModal,
    LoadingModal
  },
  data: () => ({
    //
  }),
}
</script>
