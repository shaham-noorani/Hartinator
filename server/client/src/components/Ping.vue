<template>
  <div class="col">
    <h1 class="heading">Hartinator</h1>
    <form @submit="postProgression">
    <label>
      Key:
    <input v-model="key"/>
    </label>
    <br>
    <label>
      Progression:
    <input v-model="progression"/>
    <button class="submit" type="submit">Enter</button>
    </label>
    <br>
    <h2 class="voices-heading">Voices</h2>
    <p>Soprano: {{ voices["soprano"] }}</p>
    <p>Alto: {{ voices["alto"] }}</p>
    <p>Tenor: {{ voices["tenor"] }}</p>
    <p>Bass: {{ voices["bass"] }}</p>
  </form>
  <!-- <pdf src="../../python/artifacts/cave.pdf" ></pdf> -->
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import pdf from 'vue-pdf';

export default {
  name: 'Ping',
  data() {
    return {
      voices: {
          "soprano": "",
          "alto": "",
          "tenor": "",
          "bass": ""
      },
      key: '',
      progression: '',
      pdf: '',
    };
  },
  methods: {
    getNotes() {
      const notesPath = 'http://localhost:5000/notes';
      axios.get(notesPath)
        .then((res) => {
          this.voices["soprano"] = res.data.voices["soprano"]
          this.voices["alto"] = res.data.voices["alto"]
          this.voices["tenor"] = res.data.voices["tenor"]
          this.voices["bass"] = res.data.voices["bass"]
        })
        .catch((error) => {
        console.error(error);
        });
    },
    getPDF ()
    {
      const notesPath = 'http://localhost:5000/notes';
      axios.get(notesPath)
        .then((res) => {
          this.pdf = "../../python/artifacts/" + res.data.pdf
        })
        .catch((error) => {
        console.error(error);
        });
    },
    postProgression() {
      const notesPath = 'http://localhost:5000/notes';
      axios.post(notesPath, {
        key: this.key,
        progression: this.progression,
      })
        .then(() => {
          this.getNotes();
        });
    },
  },
  created() {
    this.getNotes();
    this.getPDF();
  },
};
</script>
<style scoped>
.submit {
    margin-left: 20px;
}

.heading {
    margin-bottom: 40px;
}

.voices-heading {
    margin-top: 40px;
}
</style>
