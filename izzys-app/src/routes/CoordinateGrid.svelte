<!-- <script>
    import { onMount } from 'svelte';
    import axios from 'axios';
  
    let characters = [];
  
    onMount(async () => {
      try {
        const response = await axios.get('https://your-django-api-url.com/character-positions');
        characters = response.data;
      } catch (error) {
        console.error('Error fetching character positions:', error);
      }
    });
  </script>
  
  

  <svg width="160" height="128">
    {#each characters as character (character.id)}
      <circle
        cx={character.x}
        cy={character.y}
        r="3"
        fill="blue"
      />
    {/each}
  </svg>  -->


  