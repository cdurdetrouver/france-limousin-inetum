<script lang="ts">
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	let display_mode = 0;

	let idanimal: string;
	let prediction: {
		labeco2: string;
		labeco3: string;
		naissance: number;
		poids: number;
		prix: number;
	} = { labeco2: '', labeco3: '', naissance: 0, poids: 0, prix: 0 };

	let start_time: number;

	async function request(idanimal: string) {
		try {
			const response = await fetch('http://localhost:5000/prediction_id', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ id: idanimal })
			});

			if (!response.ok) {
				const errorData = await response.json();
				const t = {
					message: 'Erreur: ' + errorData.error,
					background: 'variant-filled-error'
				};
				toastStore.trigger(t);
				setTimeout(
					() => {
						display_mode = 0;
					},
					Math.max(0, start_time + 1000 - Date.now())
				);
				return null;
			}

			const data = await response.json();
			prediction = {
				labeco2: data['p_libeco2'],
				labeco3: data['p_libeco3'],
				naissance: data['p_pnc'],
				poids: data['p_p210'],
				prix: data['p_enchere']
			};
			return prediction;
		} catch (error) {
			const t: ToastSettings = {
				message: 'Erreur: ' + (error as Error).message,
				background: 'variant-filled-error'
			};
			toastStore.trigger(t);
			setTimeout(
				() => {
					display_mode = 0;
				},
				Math.max(0, start_time + 1000 - Date.now())
			);
			return null;
		}
	}

	function make_prediction(event: Event) {
		if (!/^\d{6}$/.test(idanimal)) {
			const t: ToastSettings = {
				message: "L'id animal devrait seulement être composé de nombres",
				background: 'variant-filled-error'
			};
			toastStore.trigger(t);
			return;
		}

		event.preventDefault();
		display_mode = 1;
		start_time = Date.now();
		request(idanimal).then((data) => {
			if (data !== null) {
				setTimeout(
					() => {
						display_mode = 2;
					},
					Math.max(0, start_time + 1000 - Date.now())
				);
			}
		});
	}
</script>

<div class="h-full flex items-center justify-center">
	{#if display_mode == 0}
		<form class="flex gap-10 items-center justify-between" on:submit={make_prediction}>
			<input
				class="input p-4 pb-2 pt-2 w-auto"
				type="search"
				name="demo"
				placeholder="Id de l'animal"
				bind:value={idanimal}
			/>
			<button type="submit" class="btn btn-lg variant-filled-primary"
				>Générer la prédiction ✨</button
			>
		</form>
	{:else if display_mode == 1}
		<div class="flex flex-col gap-10 items-center justify-between">
			<ProgressBar />
			<h1 class="h1">Génération de la réponse</h1>
		</div>
	{:else if display_mode == 2}
		<div class="flex flex-col gap-10 items-center justify-between">
			<div class="card card-hover overflow-hidden text-2xl">
				<header>
					<img
						src="champ.jpg"
						class="bg-black/50 h-full aspect-[21/9] overflow-hidden"
						alt="Post"
					/>
				</header>
				<div class="p-4 space-y-4">
					<h6 class="h3" data-toc-ignore>Prédiction</h6>
					<h3 class="h2" data-toc-ignore>Animal id : {idanimal}</h3>
					<article>
						<p>Libeco2 : {prediction.labeco2}</p>
						<p>Libeco3 : {prediction.labeco3}</p>
						<p>Poids à la naissance : {prediction.naissance}</p>
						<p>Poids 210 jours : {prediction.poids}</p>
						<p>Prix : {prediction.prix}</p>
					</article>
				</div>
			</div>
			<button
				type="button"
				class="btn variant-filled-primary"
				on:click={() => {
					display_mode = 0;
				}}>Nouvelle Prédiction</button
			>
		</div>
	{/if}
</div>
