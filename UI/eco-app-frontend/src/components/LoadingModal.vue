<template>
    <v-row justify="space-around">
        <v-col cols="auto">
            <v-dialog
                    transition="dialog-top-transition"
                    v-model="isVisible"
            >
                <v-card>
                    <v-card-text>
                        <div class="text-h6 pa-12" v-if="isVisible">
                            <v-progress-circular
                                    :size="70"
                                    :width="7"
                                    color="purple"
                                    indeterminate
                                    class="pa-12"
                            ></v-progress-circular>
                        </div>
                    </v-card-text>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name:"LadingModal",
        computed: {
            isVisible(){
                return this.$store.state.loader
            }
        }
    }
</script>
