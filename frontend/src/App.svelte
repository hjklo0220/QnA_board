<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"

  const routes = {
    '/': Home,
    '/:question_id': Detail,
  }

</script>

<Router {routes}/>