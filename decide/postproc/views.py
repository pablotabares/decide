import random
from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weight(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weightedRandomSelection(self, options):
        out = []
        n_votes = 0
        for opt in options:
            n_votes += opt["votes"]

        if n_votes == 0:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': False
                })
            return Response(out)

        random_value = random.randint(0, n_votes-1)
        found = False
        for i in range(0, len(options)):
            random_value -= options[i]["votes"]
            if random_value < 0 and not found:
                out.append({
                    **options[i],
                    'postproc': True
                })
                found = True
            else:
                out.append({
                    **options[i],
                    'postproc': False
                })
        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def hondt(self, options, seats):
        out = []
        votes = []
        assignment = []
        votescount = 0

        for opt in options:
            votescount += opt['votes'];
            votes.append({
                'votes': opt['votes'],
            })
            assignment.append({
                'seats': 0
            })

        for i in range(seats):
            max = 0;
            imax = 0;
            for i in range(len(votes)):
                cociente = votes[i]['votes'] / (assignment[i]['seats'] + 1)
                if (cociente > max):
                    max = cociente
                    imax = i
            assignment[imax]['seats'] += 1
        for i in range(len(options)):
            if(votescount != 0):
                out.append({
                    **options[i],
                    'postproc': assignment[i]['seats'],
                })
            else:
                out.append({
                    **options[i],
                    'postproc': 0,
                })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def borda(self, options):
        option_positions = {} # {'A': [1,1,2], 'B':[2,2,1]}
        out = {} # {'A':'5', 'B':'4'}
        if len(options) != 0:
            if len(options[0]['positions']) != 0:
                for opt in options:
                    opcion = opt['option']
                    posiciones = opt['positions']
                    option_positions[opcion] = posiciones

                # We add 1; we have 2 options, so value of vote position 1 is 2 and vote 
                # position 2 is 1. I want to do 2+1 - position. First position 3-1=2 points
                noptions = len(options) + 1
                for opt_p in option_positions:
                    suma = 0
                    for p in option_positions.get(opt_p): #We caugth positions [1,1,2]
                        suma += noptions - p #We add points
                        
                    out[opt_p] = suma 
            else: #If we haven't got any votes win the first option
                valor = len(options)
                for opt in options:
                    opcion = opt['option']
                    out[opcion] = valor
                    valor = valor - 1

        return Response(out)

    def multiquestion(self, questions):
        out = []

        for question in questions:
            votes = []

            for opt in question['options']:
                votes.append({
                    **opt,
                    'postproc': opt['votes'],
                })

            votes.sort(key=lambda x: -x['postproc'])
            out.append({
                'text': question['text'],
                'options': votes
            })
        return Response(out)

    def add_first(self, first_list, second_list):
        """
            This function alternate the elements of the first list and the second list. The first element of the
            new list will be the first element of the first list.
        """
        pos = 0
        out = []
        for i in range(0, max(len(first_list), len(second_list))):
            if i < len(first_list):
                out.append({
                    **first_list[i],
                    'postproc': pos+1,
                })
                pos += 1
            if i < len(second_list):
                out.append({
                    **second_list[i],
                    'postproc': pos+1,
                })
                pos += 1
        return out

    def genderBalanced(self, options):
        data_in = options
        data_in.sort(key=lambda x: -x['votes'])
        out = []

        # If there is no votes, 'postproc' will be 0 in all the options
        if data_in[0]['votes'] == 0:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': 0
                })
            return Response(out)


        male_list = [x for x in data_in if x['gender'] == 'MALE']
        female_list = [x for x in data_in if x['gender'] == 'FEMALE']

        # If there is no male or female options in the voting
        if not female_list or not male_list:
            return Response(self.add_first(male_list, female_list))

        # If the most voted option is a man
        if male_list[0]['votes'] > female_list[0]['votes']:
            return  Response(self.add_first(male_list, female_list))
        elif male_list[0]['votes'] == female_list[0]['votes']:
            out = self.add_first(male_list, female_list) if random.randint(0, 1) else self.add_first(female_list, male_list)
            return Response(out)
        else:
            # If the most voted option is a woman
            return Response(self.add_first(female_list, male_list))

    def droop_quota(self, options, seats):
        out = []
        n_votes = sum(x["votes"] for x in options)

        if n_votes == 0:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': 0
                })
            return Response(out)

        cociente = n_votes/(seats+1) + 1
        cociente = int(cociente)+1 if cociente - int(cociente) >= 0.5 else int(cociente)

        asignados = {}
        n_asignados = 0
        temp = {}
        for o in options:
            asignados[o["option"]] = int(o["votes"]/cociente)
            n_asignados += int(o["votes"]/cociente)
            temp[o["option"]] = o["votes"]%cociente

        k = seats - n_asignados
        while k > 0:
            asignados[max(temp, key=temp.get)] += 1
            temp.pop(max(temp, key=temp.get))
            k -= 1

        for o in options:
            out.append({
                **o,
                'postproc': asignados[o["option"]]
            })

        return Response(out)

    def sainte_lague(self, options, seats):
        out = {}
        nOptions = len(options)
        calculos = []        
        if nOptions != 0: # if we don't get any options, do nothing
            for opt in options: # Get all options and initilize 0. Get all votes
                opcion = opt['option']
                out[opcion] = 0

                calculos.append(opt['votes'])

            cociente = 1
            escano = 1 
            while escano <= seats: # Distribute all the seats
                maximo = max(calculos) 
                indice_maximo = calculos.index(maximo) # Get index of maximo
                out[options[indice_maximo]['option']] += 1 # Add 1 this option
                calculos[indice_maximo] = maximo / cociente 

                cociente += 2
                escano += 1
        
        return Response(out)


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | BORDA
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t =='WEIGHT':
            return self.weight(opts)
        elif t == 'WEIGHTED-RANDOM':
            return self.weightedRandomSelection(opts)
        elif t == 'HONDT':
            seats = request.data.get('seats', 1)
            return self.hondt(opts, seats)
        elif t == 'BORDA':
            return self.borda(opts)
        elif t == 'MULTIPLE':
            questions = request.data.get('questions', [])
            return self.multiquestion(questions)
        elif t == 'GENDER-BALANCED':
            return self.genderBalanced(opts)
        elif t == 'DROOP':
            seats = request.data.get('seats', 1)
            return self.droop_quota(opts, seats)
        elif t == 'SAINTE-LAGUE':
            seats = request.data.get('seats', 1)
            return self.sainte_lague(opts, seats)

        return Response({})
