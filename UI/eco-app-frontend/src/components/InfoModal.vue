<template>
    <v-row justify="space-around">
        <v-col cols="auto">
            <v-dialog
                    transition="dialog-top-transition"
                    v-model="isVisible"
            >
            <v-card>
                <v-toolbar
                        color="primary"
                        dark
                >{{modalTitle}}</v-toolbar>
                <v-card-text>
                    <div class="text-h6 pa-12">{{modalInfo}}</div>
                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn
                            text
                            @click="hideModal"
                    >Close</v-btn>
                </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name:"InfoModal",
        // props: ["type", "detail"],
        computed: {
            isVisible(){
                return this.$store.state.modalInfo.isVisible
            },
            modalTitle(){
                return this.$store.state.modalInfo.ModalTitle
            },
            modalInfo(){
                return this.$store.state.modalInfo.ModalInfo.detail
            }
        },
        methods:{
            hideModal(){
                this.$store.commit("SET_MODAL_DATA",
                    {
                        isVisible:false,
                        ModalTitle:"",
                        ModalInfo:{detail:""}
                    })
            }
        }
    }
</script>
